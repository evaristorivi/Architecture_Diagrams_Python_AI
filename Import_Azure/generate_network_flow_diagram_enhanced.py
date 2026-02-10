#!/usr/bin/env python3
"""
Azure Network Flow Diagram Generator (Enhanced)
Generates professional network topology diagrams from Azure infrastructure JSON export.

Features:
- Hub-Spoke topology detection
- VMs with private IP addresses
- NSGs displayed at NIC level and subnet level with rule summaries
- Private Endpoints and traffic flows
- Professional muted color scheme
- Outputs: PNG, DOT, DrawIO formats

Layout: TOP-DOWN
    Internet (top)
        ↓ HTTPS to external LBs
    Hub VNet (firewall VM for routing)
        ↓ VNet Peering (all traffic routes through hub)
    Spoke VNets (web/app tiers with LBs, VMSS, SQL, KV)
"""

import json
import os
import subprocess
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
import shutil

from diagrams import Diagram, Cluster, Edge
from diagrams.azure.compute import VM, VMScaleSet
from diagrams.azure.network import (
    VirtualNetworks, Subnets, LoadBalancers,
    PublicIpAddresses, Firewall, VirtualNetworkGateways,
    PrivateEndpoint,
)
from diagrams.azure.database import SQLServers
from diagrams.azure.security import KeyVaults
from diagrams.azure.storage import StorageAccounts
from diagrams.onprem.network import Internet


# Professional muted color scheme (enterprise style)
COLORS = {
    'hub_vnet': '#E8E8E8',           # Light gray
    'spoke_vnet': '#F5F5F5',         # Very light gray
    'subscription': '#FAFAFA',       # Near white
    'resource_group': '#FFFFFF',     # White
    'firewall_subnet': '#E0E0E0',    # Slightly darker gray
    'web_subnet': '#F0F0F0',         # Light gray
    'app_subnet': '#F0F0F0',         # Light gray
    'data_subnet': '#F0F0F0',        # Light gray
    'pe_subnet': '#F0F0F0',          # Light gray
    'default_subnet': '#FFFFFF',     # White
    'internet': '#E8E8E8',           # Light gray
}


class AzureNetworkDiagramGenerator:
    def __init__(self, input_file: str, output_name: str = "network_flow_diagram"):
        self.input_file = input_file
        self.output_name = output_name
        self.output_dir = Path("diagrams")
        self.output_dir.mkdir(exist_ok=True)

        self.infrastructure: Dict = {}
        
        # Internal state
        self.vnet_map: Dict[str, Dict] = {}
        self.subnet_map: Dict[str, Dict] = {}
        self.nic_subnet_map: Dict[str, str] = {}
        self.nic_ip_map: Dict[str, str] = {}
        self.resource_subnet_map: Dict[str, str] = {}
        self.nsg_id_map: Dict[str, Dict] = {}
        self.nic_nsg_map: Dict[str, Dict] = {}
        
        self.hub_vnets: Set[str] = set()
        self.spoke_vnets: Set[str] = set()
        self.peerings: List[Dict] = []
        self.private_endpoints: List[Dict] = []

        self.nodes: Dict[str, object] = {}
        self.vnet_nodes: Dict[str, object] = {}
        self.drawn_peerings: Set[Tuple[str, str]] = set()

        # Track for traffic flows
        self.external_lbs: List = []
        self.hub_fw_nodes: List = []
        self.spoke_lbs: List = []

        # Status tracking
        self.total_resources = 0

    def print_status(self, emoji: str, message: str):
        """Print status message with emoji"""
        print(f"{emoji} {message}")

    def load_infrastructure(self):
        self.print_status("📂", f"Loading {self.input_file}...")
        
        if not Path(self.input_file).exists():
            self.print_status("❌", f"File not found: {self.input_file}")
            return False
        
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                self.infrastructure = json.load(f)
            self.print_status("✅", "Infrastructure loaded")
            
            subs = self.infrastructure.get("subscriptions", [])
            self.print_status("📊", f"{len(subs)} subscription(s)")
            return True
            
        except json.JSONDecodeError as e:
            self.print_status("❌", f"Invalid JSON: {e}")
            return False

    def analyze_topology(self):
        self.print_status("🔍", "Analyzing topology...")
        
        for sub in self.infrastructure.get("subscriptions", []):
            sub_id = sub.get("subscriptionId", "")
            sub_name = sub.get("displayName", "")
            
            for rg in sub.get("resourceGroups", []):
                rg_name = rg.get("resourceGroupName", "")
                resources = rg.get("resources", {})
                net = resources.get("network", {})
                compute = resources.get("compute", {})

                # Index NICs and extract IPs
                self._index_nics(net)
                
                # Index NSGs
                self._index_nsgs(net)
                
                # Index VNets and subnets
                self._index_vnets(net, rg_name, sub_name, sub_id, resources)
                
                # Index other resources
                self._index_resources(resources, rg_name)
                
                # Map resources → subnets
                self._map_resources(rg)

        # Detect hub/spoke topology
        self._detect_hub_spoke()
        
        # Collect peerings from VNets
        self._collect_peerings()
        
        self.print_status("✅", f"Analysis complete: {self.total_resources} resources")

    def _index_nics(self, net: Dict):
        """Index NICs and extract IP addresses"""
        nics = net.get("networkInterfaces", [])
        
        for nic in nics:
            nic_id = nic.get('id', '').lower()  # Normalize to lowercase for case-insensitive lookup
            ip_configs = nic.get('ip_configurations', [])
            
            if ip_configs:
                subnet_id = ip_configs[0].get('subnet', {}).get('id')
                private_ip = ip_configs[0].get('private_ip_address')
                
                if subnet_id:
                    self.nic_subnet_map[nic_id] = subnet_id
                if private_ip:
                    self.nic_ip_map[nic_id] = private_ip

    def _index_nsgs(self, net: Dict):
        """Index NSGs and their rules"""
        nsgs = net.get("networkSecurityGroups", [])
        nics = net.get("networkInterfaces", [])
        
        # Create a map of NSG ID -> NSG data
        for nsg in nsgs:
            nsg_id = nsg.get('id')
            nsg_name = nsg.get('name', 'Unknown')
            rules = nsg.get('security_rules', [])
            
            # Extract key rules for summary
            summary = self._summarize_nsg_rules(rules)
            
            self.nsg_id_map[nsg_id] = {
                'name': nsg_name,
                'id': nsg_id,
                'summary': summary
            }
            
            self.print_status("🔒", f"NSG '{nsg_name}': {summary}")
        
        # Index NIC-level NSGs
        for nic in nics:
            nic_id = nic.get('id', '').lower()  # Normalize to lowercase
            nsg_ref = nic.get('network_security_group', {})
            if nsg_ref:
                nsg_id = nsg_ref.get('id')
                if nsg_id and nsg_id in self.nsg_id_map:
                    self.nic_nsg_map[nic_id] = self.nsg_id_map[nsg_id]
                    self.print_status("🔗", f"NIC {nic.get('name', 'NIC')}: NSG {self.nsg_id_map[nsg_id].get('summary', 'N/A')}")

    def _summarize_nsg_rules(self, rules: List[Dict]) -> str:
        """Summarize NSG rules into a brief label"""
        if not rules:
            return "Default Rules"
        
        allowed_ports = set()
        
        for rule in rules:
            if rule.get('access', '').lower() == 'allow':
                dst_ports = rule.get('destination_port_range', '*')
                
                # Map common ports to protocol names
                if dst_ports == '80':
                    allowed_ports.add('HTTP')
                elif dst_ports == '443':
                    allowed_ports.add('HTTPS')
                elif dst_ports == '22':
                    allowed_ports.add('SSH')
                elif dst_ports == '3389':
                    allowed_ports.add('RDP')
                elif dst_ports == '3306':
                    allowed_ports.add('MySQL')
                elif dst_ports == '5432':
                    allowed_ports.add('PostgreSQL')
                elif dst_ports == '1433':
                    allowed_ports.add('MSSQL')
                elif dst_ports != '*':
                    allowed_ports.add(f"Port:{dst_ports}")
        
        if allowed_ports:
            return f"Allow: {', '.join(sorted(allowed_ports))}"
        return "Default Rules"

    def _index_vnets(self, net: Dict, rg_name: str, sub_name: str, sub_id: str, resources: Dict):
        """Index Virtual Networks and subnets"""
        vnets = net.get("virtualNetworks", [])
        
        for vnet in vnets:
            vnet_id = vnet.get('id')
            vnet_name = vnet.get('name', 'Unknown')
            address_space = vnet.get('address_space', {}).get('address_prefixes', [])
            cidr = address_space[0] if address_space else 'N/A'
            
            # Store VNet data
            self.vnet_map[vnet_id] = {
                'name': vnet_name,
                'id': vnet_id,
                'rg_name': rg_name,
                'sub_name': sub_name,
                'sub_id': sub_id,
                'cidr': cidr,
                'subnets': {},
                'peerings': vnet.get('virtual_network_peerings', []),
                'firewalls': [],
                'gateways': [],
                'compute': resources.get('compute', {}),
                'network': net,
                'sql': resources.get('sql', {}),
                'keyvault': resources.get('keyvault', {}),
            }
            
            # Index subnets
            subnets = vnet.get('subnets', [])
            for subnet in subnets:
                subnet_id = subnet.get('id')
                subnet_name = subnet.get('name', 'Unknown')
                subnet_prefix = subnet.get('address_prefix', 'N/A')
                
                self.subnet_map[subnet_id] = {
                    'name': subnet_name,
                    'id': subnet_id,
                    'vnet_id': vnet_id,
                    'vnet_name': vnet_name,
                    'prefix': subnet_prefix,
                    'nsg': subnet.get('network_security_group'),
                }
                
                self.vnet_map[vnet_id]['subnets'][subnet_id] = subnet

    def _index_resources(self, resources: Dict, rg_name: str):
        """Index compute and other resources"""
        # VMs
        compute = resources.get('compute', {})
        vms = compute.get('virtualMachines', [])
        
        for vm in vms:
            self.total_resources += 1
            vm_id = vm.get('id')
            # Find subnet via NIC
            nics = vm.get('network_profile', {}).get('network_interfaces', [])
            if nics:
                nic_id = nics[0].get('id', '').lower()  # Normalize to lowercase
                if nic_id in self.nic_subnet_map:
                    self.resource_subnet_map[vm_id] = self.nic_subnet_map[nic_id]
        
        # VMSS
        vmss_list = compute.get('virtualMachineScaleSets', [])
        for vmss in vmss_list:
            self.total_resources += 1
            vmss_id = vmss.get('id')
            # Find subnet via profile
            profile = vmss.get('virtual_machine_profile', {})
            net_config = profile.get('network_profile', {}).get('network_interface_configurations', [])
            if net_config:
                ip_config = net_config[0].get('ip_configurations', [])
                if ip_config:
                    subnet_id = ip_config[0].get('subnet', {}).get('id')
                    if subnet_id:
                        self.resource_subnet_map[vmss_id] = subnet_id
        
        # Load Balancers
        lbs = resources.get('network', {}).get('loadBalancers', [])
        for lb in lbs:
            self.total_resources += 1
            lb_id = lb.get('id')
            # Find subnet
            frontend_configs = lb.get('frontend_ip_configurations', [])
            if frontend_configs:
                subnet_id = frontend_configs[0].get('subnet', {}).get('id')
                if subnet_id:
                    self.resource_subnet_map[lb_id] = subnet_id
        
        # SQL Servers
        sql_servers = resources.get('sql', {}).get('servers', [])
        self.total_resources += len(sql_servers)
        
        # Key Vaults
        kv = resources.get('keyvault', {}).get('vaults', [])
        self.total_resources += len(kv)
        
        # Storage Accounts
        storage = resources.get('storage', {}).get('storageAccounts', [])
        self.total_resources += len(storage)
        
        # Private Endpoints
        pe_list = resources.get('network', {}).get('privateEndpoints', [])
        for pe in pe_list:
            self.total_resources += 1
            pe_id = pe.get('id')
            subnet_id = pe.get('subnet', {}).get('id')
            if subnet_id:
                self.resource_subnet_map[pe_id] = subnet_id
            self.private_endpoints.append({
                "id": pe.get('id', ""),
                "name": pe.get('name', ""),
                "subnet_id": subnet_id,
                "connections": pe.get('private_link_service_connections', []),
            })

    def _detect_hub_spoke(self):
        """Detect hub and spoke VNets"""
        for vnet_id, vnet_data in self.vnet_map.items():
            vnet_name = vnet_data['name'].lower()
            
            # Hub detection criteria
            is_hub = False
            
            # Check name
            if 'hub' in vnet_name:
                is_hub = True
            
            # Check for firewall
            network = vnet_data['network']
            firewalls = network.get('firewalls', [])
            if firewalls:
                is_hub = True
                vnet_data['firewalls'] = firewalls
            
            # Check for gateways
            gateways = network.get('virtualNetworkGateways', [])
            if gateways:
                is_hub = True
                vnet_data['gateways'] = gateways
            
            # Check subnets for fw/gateway names
            for subnet_data in vnet_data['subnets'].values():
                subnet_name = subnet_data.get('name', '').lower()
                if any(x in subnet_name for x in ['firewall', 'gateway', 'fw', 'azurefirewall']):
                    is_hub = True
            
            if is_hub:
                self.hub_vnets.add(vnet_id)
            else:
                self.spoke_vnets.add(vnet_id)
        
        self.print_status("🏢", f"Detected {len(self.hub_vnets)} Hub VNet(s), {len(self.spoke_vnets)} Spoke VNet(s)")

    def _collect_peerings(self):
        """Collect all VNet peerings"""
        for vnet_id, vnet_data in self.vnet_map.items():
            for peer in vnet_data.get('peerings', []):
                remote_id = peer.get("remote_virtual_network", {}).get("id", "")
                if remote_id:
                    self.peerings.append({
                        "source": vnet_id,
                        "target": remote_id,
                        "state": peer.get("peering_state", "Unknown"),
                    })

    def _map_resources(self, rg: Dict):
        compute = rg.get("resources", {}).get("compute", {})
        network = rg.get("resources", {}).get("network", {})

        for vm in compute.get("virtualMachines", []):
            vm_id = vm.get("id", "")
            nics = vm.get("network_profile", {}).get("network_interfaces", [])
            if nics:
                nic_id = nics[0].get("id", "")
                if nic_id in self.nic_subnet_map:
                    self.resource_subnet_map[vm_id] = self.nic_subnet_map[nic_id]

        for vmss in compute.get("virtualMachineScaleSets", []):
            vmss_id = vmss.get("id", "")
            nic_cfgs = (vmss.get("virtual_machine_profile", {})
                            .get("network_profile", {})
                            .get("network_interface_configurations", []))
            if nic_cfgs:
                ip_cfgs = nic_cfgs[0].get("ip_configurations", [])
                if ip_cfgs:
                    sid = ip_cfgs[0].get("subnet", {}).get("id", "")
                    if sid:
                        self.resource_subnet_map[vmss_id] = sid

        for lb in network.get("loadBalancers", []):
            lb_id = lb.get("id", "")
            fe_cfgs = lb.get("frontend_ip_configurations", [])
            if fe_cfgs:
                sid = fe_cfgs[0].get("subnet", {}).get("id", "")
                if sid:
                    self.resource_subnet_map[lb_id] = sid

    def generate_diagram(self):
        self.print_status("🎨", "Generating diagram...")
        
        # Check for GraphViz
        if not self._check_graphviz():
            self.print_status("❌", "GraphViz is not installed or not on PATH")
            self.print_status("📥", "Install GraphViz:")
            self.print_status("   ", "Option 1 - Using Chocolatey: choco install graphviz")
            self.print_status("   ", "Option 2 - Download installer: https://graphviz.org/download/")
            sys.exit(1)
        
        output_path = str(self.output_dir / self.output_name)

        graph_attr = {
            "splines": "ortho",
            "nodesep": "0.8",
            "ranksep": "1.2",
            "fontsize": "14",
            "fontname": "Segoe UI",
            "bgcolor": "white",
            "pad": "0.8",
            "compound": "true",
            "rankdir": "TB",
        }

        with Diagram(
            name="Azure Network Flow Diagram",
            filename=output_path,
            show=False,
            direction="TB",
            graph_attr=graph_attr,
            node_attr={"fontsize": "10", "fontname": "Segoe UI"},
            edge_attr={"fontsize": "9", "fontname": "Segoe UI"},
            outformat=["png", "dot"],
        ):
            # ══════════════════════════════════════════════════════════
            # INTERNET (TOP)
            # ══════════════════════════════════════════════════════════
            with Cluster("External", graph_attr={"bgcolor": COLORS['internet'], "style": "rounded", "margin": "15"}):
                internet = Internet("Internet\nUsers")

            # ══════════════════════════════════════════════════════════
            # SUBSCRIPTIONS with Hub at top, Spokes below
            # ══════════════════════════════════════════════════════════
            # Group VNets by subscription
            subs_data = {}
            for vid, vdata in self.vnet_map.items():
                sub_name = vdata.get("sub_name", "Unknown")
                if sub_name not in subs_data:
                    subs_data[sub_name] = {"hub": [], "spoke": []}
                if vid in self.hub_vnets:
                    subs_data[sub_name]["hub"].append(vdata)
                else:
                    subs_data[sub_name]["spoke"].append(vdata)

            # Render subscriptions
            for sub_name, vnets in subs_data.items():
                with Cluster(f"☁️ {sub_name}", graph_attr={
                    "bgcolor": COLORS['subscription'], "style": "rounded", "margin": "20", "fontsize": "14"
                }):
                    # Hub VNets first
                    for vdata in vnets["hub"]:
                        self._render_vnet(vdata, is_hub=True)

                    # Spoke VNets
                    for vdata in vnets["spoke"]:
                        self._render_vnet(vdata, is_hub=False)

            # ══════════════════════════════════════════════════════════
            # TRAFFIC FLOWS
            # ══════════════════════════════════════════════════════════
            
            # Internet → External LBs (HTTPS)
            for lb in self.external_lbs[:4]:
                internet >> Edge(label="HTTPS", color="green", style="bold", penwidth="2") >> lb

            # Hub FW → Internal traffic routing (all spoke traffic goes through hub)
            if self.hub_fw_nodes and self.spoke_lbs:
                for lb in self.spoke_lbs[:4]:
                    self.hub_fw_nodes[0] >> Edge(
                        label="Routed\nTraffic", color="blue", style="dashed", penwidth="1.5"
                    ) >> lb

            # VNet Peerings
            self._draw_peerings()

            # Private Endpoint → SQL/KV
            for pe in self.private_endpoints:
                pe_id = pe["id"]
                if pe_id in self.nodes:
                    pe_node = self.nodes[pe_id]
                    for conn in pe.get("connections", []):
                        target_id = conn.get("private_link_service_id", "")
                        if target_id in self.nodes:
                            pe_node >> Edge(label="Private\nLink", color="orange", style="bold") >> self.nodes[target_id]

        self.print_status("✅", f"{output_path}.png")
        self.print_status("✅", f"{output_path}.dot")
        self._convert_to_drawio(output_path)

    def _render_vnet(self, vdata: Dict, is_hub: bool):
        vid = vdata.get("id", "")
        vname = vdata.get("name", "VNet")
        cidrs = vdata.get("address_space", {}).get("address_prefixes", [])
        cidr_str = ", ".join(cidrs) if cidrs else vdata.get('cidr', 'N/A')
        rg_name = vdata.get("rg_name", "")

        color = COLORS['hub_vnet'] if is_hub else COLORS['spoke_vnet']
        icon = "🏢 HUB" if is_hub else "🌐 SPOKE"

        compute = vdata.get("compute", {})
        network = vdata.get("network", {})
        sql_res = vdata.get("sql", {})
        kv_res = vdata.get("keyvault", {})

        all_nodes = []

        with Cluster(f"📂 {rg_name}", graph_attr={"bgcolor": COLORS['resource_group'], "style": "rounded", "margin": "15", "fontsize": "11"}):
            with Cluster(f"{icon}: {vname}\n{cidr_str}", graph_attr={
                "bgcolor": color, "style": "rounded", "margin": "15", "fontsize": "11"
            }):
                for subnet_id, subnet_data in vdata.get("subnets", {}).items():
                    nodes = self._render_subnet(subnet_data, network, compute, is_hub)
                    all_nodes.extend(nodes)

                # SQL Servers (inside VNet cluster, in data subnet area)
                for srv in sql_res.get("servers", []):
                    srv_id = srv.get("id", "")
                    if srv_id not in self.nodes:
                        dbs = [d["name"] for d in sql_res.get("databases", []) if d.get("name") != "master"]
                        label = f"{srv['name']}\n({', '.join(dbs)})" if dbs else srv['name']
                        node = SQLServers(label)
                        self.nodes[srv_id] = node
                        all_nodes.append(node)

                # Key Vaults (inside VNet cluster)
                for kv in kv_res.get("vaults", []):
                    kv_id = kv.get("id", "")
                    if kv_id not in self.nodes:
                        node = KeyVaults(kv["name"])
                        self.nodes[kv_id] = node
                        all_nodes.append(node)

        # Representative node for peering
        rep = all_nodes[0] if all_nodes else VirtualNetworks(vname)
        self.vnet_nodes[vid] = rep

    def _render_subnet(self, sn: Dict, network: Dict, compute: Dict, is_hub: bool) -> List:
        sn_id = sn.get("id", "")
        sn_name = sn.get("name", "Subnet")
        sn_cidr = sn.get("address_prefix", "") or sn.get("prefix", "N/A")
        low = sn_name.lower()

        # Get NSG info for subnet level
        nsg_label = ""
        nsg_ref = sn.get('network_security_group', {}) or sn.get('nsg', {})
        
        if nsg_ref:
            nsg_id = nsg_ref.get('id')
            if nsg_id and nsg_id in self.nsg_id_map:
                nsg_info = self.nsg_id_map[nsg_id]
                nsg_name = nsg_info.get('name', 'NSG')
                summary = nsg_info.get('summary', 'No Rules')
                nsg_label = f"\n🔒 NSG: {nsg_name}\n   {summary}"
                self.print_status("✅", f"  ✓ NSG rendered: {nsg_name}")
            else:
                self.print_status("❌", f"  ✗ NSG ID not in map")
        else:
            self.print_status("⚠️", f"  No NSG on subnet")

        # Color by purpose
        if "firewall" in low or "fw" in low:
            color = COLORS['firewall_subnet']
        elif "web" in low or "ingress" in low:
            color = COLORS['web_subnet']
        elif "app" in low:
            color = COLORS['app_subnet']
        elif "data" in low:
            color = COLORS['data_subnet']
        elif "pe" in low or "endpoint" in low:
            color = COLORS['pe_subnet']
        else:
            color = COLORS['default_subnet']

        # Create subnet label with NSG info
        label = f"{sn_name}\n{sn_cidr}{nsg_label}"

        nodes = []

        with Cluster(label, graph_attr={"bgcolor": color, "margin": "10", "fontsize": "9"}):
            
            # Create NSG label node if subnet has NSG
            nsg_node = None
            if nsg_label:
                nsg_node = Subnets(nsg_label.replace("\n", " ").replace("   ", ""))
                nodes.append(nsg_node)
            # VMs (firewall VM in hub)
            for vm in compute.get("virtualMachines", []):
                vm_id = vm.get("id", "")
                if self.resource_subnet_map.get(vm_id) == sn_id:
                    name = vm.get("name", "VM")
                    size = vm.get("hardware_profile", {}).get("vm_size", "")
                    
                    # Add IP address and NIC-level NSG info
                    label_parts = [name]
                    
                    # Get IP address
                    ip = None
                    nics = vm.get("network_profile", {}).get("network_interfaces", [])
                    nic_nsg_label = None
                    
                    if nics:
                        nic_id = nics[0].get("id", "").lower()
                        ip = self.nic_ip_map.get(nic_id)
                        
                        # Check for NIC-level NSG
                        nic_nsg_label = ""
                        if nic_id in self.nic_nsg_map:
                            nsg_info = self.nic_nsg_map[nic_id]
                            nsg_name = nsg_info.get('name', 'NSG')
                            summary = nsg_info.get('summary', 'No Rules')
                            nic_nsg_label = f"\n🔒 {summary}"
                            self.print_status("✅", f"    ✓ NIC NSG: {nsg_name}")
                        else:
                            self.print_status("⚠️", f"    No NIC-level NSG")
                    
                    # Create simple VM label without NSG (will be separate node)
                    simple_label = f"{name}"
                    if ip:
                        simple_label += f"\n({ip})"
                    simple_label += f"\n{size}"
                    
                    # Check if this is a firewall VM
                    if "fw" in name.lower() or "firewall" in name.lower():
                        n = VM(f"🔥 {simple_label}\n(NVA)")
                        self.hub_fw_nodes.append(n)
                    else:
                        n = VM(simple_label)
                    
                    nodes.append(n)
                    self.nodes[vm_id] = n
                    
                    # Add NSG as a separate node if present
                    if nic_nsg_label:
                        nsg_info_node = Subnets(f"🔒 {name}\n{nic_nsg_label.strip()}")
                        nodes.append(nsg_info_node)

            # VMSS
            for vmss in compute.get("virtualMachineScaleSets", []):
                vmss_id = vmss.get("id", "")
                if self.resource_subnet_map.get(vmss_id) == sn_id:
                    name = vmss.get("name", "VMSS")
                    cap = vmss.get("sku", {}).get("capacity", "?")
                    n = VMScaleSet(f"{name}\nx{cap}")
                    nodes.append(n)
                    self.nodes[vmss_id] = n

            # Load Balancers
            for lb in network.get("loadBalancers", []):
                lb_id = lb.get("id", "")
                lb_name = lb.get("name", "LB")
                fe_cfgs = lb.get("frontend_ip_configurations", [])
                
                # Check if external (public IP) or internal (subnet)
                is_external = False
                if fe_cfgs:
                    pip = fe_cfgs[0].get("public_ip_address", {})
                    if pip and pip.get("id"):
                        is_external = True
                    sid = fe_cfgs[0].get("subnet", {}).get("id", "")
                    if sid == sn_id or is_external:
                        sku = lb.get("sku", {}).get("name", "")
                        if is_external:
                            lb_node = LoadBalancers(f"🌐 {lb_name}\n(External)")
                            self.external_lbs.append(lb_node)
                        else:
                            lb_node = LoadBalancers(f"{lb_name}\n(Internal)")
                            self.spoke_lbs.append(lb_node)
                        nodes.append(lb_node)
                        self.nodes[lb_id] = lb_node

                        # LB → VMSS backend
                        for pool in lb.get("backend_address_pools", []):
                            for bip in pool.get("backend_ip_configurations", []):
                                bip_id = bip.get("id", "")
                                for vmss in compute.get("virtualMachineScaleSets", []):
                                    if vmss["id"] in bip_id and vmss["id"] in self.nodes:
                                        lb_node >> Edge(label="Backend", color="blue") >> self.nodes[vmss["id"]]

            # Private Endpoints
            for pe in self.private_endpoints:
                if pe["subnet_id"] == sn_id:
                    n = PrivateEndpoint(pe["name"])
                    nodes.append(n)
                    self.nodes[pe["id"]] = n

            # Empty placeholder
            if not nodes:
                placeholder = Subnets(sn_name)
                nodes.append(placeholder)

        return nodes

    def _draw_peerings(self):
        for p in self.peerings:
            src, tgt = p["source"], p["target"]
            key = tuple(sorted([src, tgt]))
            if key in self.drawn_peerings:
                continue
            if src in self.vnet_nodes and tgt in self.vnet_nodes:
                self.drawn_peerings.add(key)
                state = p["state"]
                is_hub = src in self.hub_vnets or tgt in self.hub_vnets
                style = "bold" if is_hub else "dashed"
                self.vnet_nodes[src] >> Edge(
                    label=f"VNet Peering\n{state}", color="blue", style=style, dir="both", penwidth="2"
                ) >> self.vnet_nodes[tgt]

    def _convert_to_drawio(self, base: str):
        """Convert DOT file to DrawIO format using graphviz2drawio"""
        dot_f = f"{base}.dot"
        drawio_f = f"{base}.drawio"
        try:
            # Check if graphviz2drawio is available
            if shutil.which("graphviz2drawio"):
                subprocess.run(["graphviz2drawio", dot_f, "-o", drawio_f], check=True, capture_output=True)
                self.print_status("✅", f"{drawio_f}")
            else:
                self.print_status("⚠️", "graphviz2drawio not found. Install with: pip install graphviz2drawio")
        except subprocess.CalledProcessError as e:
            self.print_status("⚠️", f"graphviz2drawio failed: {e}")
        except Exception as e:
            self.print_status("⚠️", f"DrawIO conversion failed: {e}")

    def _check_graphviz(self) -> bool:
        """Check if GraphViz is installed and accessible."""
        # First try: Check if 'dot' is on PATH
        if shutil.which('dot'):
            return True
        
        # Second try: Check common Windows installation paths
        common_paths = [
            r"C:\Program Files\Graphviz\bin\dot.exe",
            r"C:\Program Files (x86)\Graphviz\bin\dot.exe",
            r"C:\ProgramData\chocolatey\bin\dot.exe",
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                # Add to PATH for this session
                graphviz_bin = os.path.dirname(path)
                os.environ['PATH'] = f"{graphviz_bin}{os.pathsep}{os.environ['PATH']}"
                self.print_status("✅", f"Found GraphViz at: {graphviz_bin}")
                return True
        
        return False

    def run(self):
        print("\n" + "=" * 60)
        print("🌐 Azure Network Flow Diagram Generator (Enhanced)")
        print("=" * 60)
        
        if not self.load_infrastructure():
            return False
            
        self.analyze_topology()
        self.generate_diagram()
        
        print("\n✅ Done!")
        print(f"   Total Resources: {self.total_resources}")
        print(f"   Hub VNets: {len(self.hub_vnets)}")
        print(f"   Spoke VNets: {len(self.spoke_vnets)}")
        print(f"   Diagram Nodes: {len(self.nodes)}")
        print(f"   Peerings: {len(self.peerings)}")
        print(f"   Output Directory: diagrams/")
        
        return True


def main():
    parser = ArgumentParser(
        description='Generate Azure network topology diagrams with NSG support',
        epilog='Example: python generate_network_flow_diagram_enhanced.py azure-infrastructure.json -o my_diagram'
    )
    parser.add_argument("input_file", help="Input JSON file (azure-infrastructure.json)")
    parser.add_argument("-o", "--output", default="network_flow_diagram", help="Output filename prefix")
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"❌ Not found: {args.input_file}")
        sys.exit(1)

    gen = AzureNetworkDiagramGenerator(args.input_file, args.output)
    success = gen.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()