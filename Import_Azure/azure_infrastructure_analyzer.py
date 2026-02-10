"""
Azure Infrastructure Analyzer
Parses and analyzes Azure infrastructure JSON export data
"""

import json
import os
from typing import Dict, List, Any, Optional
from collections import defaultdict
from pathlib import Path


class AzureInfrastructureAnalyzer:
    """Analyzes Azure infrastructure exported as JSON"""
    
    def __init__(self, json_file_path: str):
        """
        Initialize the analyzer with a JSON file path
        
        Args:
            json_file_path: Path to the azure-infraestructure.json file
        """
        self.json_file_path = json_file_path
        self.data = None
        self.load_data()
    
    def load_data(self) -> None:
        """Load and parse the JSON file"""
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            print(f"✓ Successfully loaded {self.json_file_path}")
        except FileNotFoundError:
            print(f"✗ File not found: {self.json_file_path}")
            raise
        except json.JSONDecodeError:
            print(f"✗ Invalid JSON format in: {self.json_file_path}")
            raise
    
    def get_subscriptions(self) -> List[Dict[str, Any]]:
        """Get all subscriptions"""
        return self.data.get('subscriptions', [])
    
    def get_resource_groups(self, subscription_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all resource groups or filter by subscription
        
        Args:
            subscription_id: Optional subscription ID to filter by
            
        Returns:
            List of resource groups
        """
        resource_groups = []
        for subscription in self.get_subscriptions():
            if subscription_id and subscription['subscriptionId'] != subscription_id:
                continue
            resource_groups.extend(subscription.get('resourceGroups', []))
        return resource_groups
    
    def count_resources_by_type(self) -> Dict[str, int]:
        """Count all resources by type"""
        resource_counts = defaultdict(int)
        
        for rg in self.get_resource_groups():
            resources = rg.get('resources', {})
            for category, items in resources.items():
                if isinstance(items, dict):
                    for resource_type, resources_list in items.items():
                        if isinstance(resources_list, list):
                            resource_counts[f"{category}.{resource_type}"] += len(resources_list)
        
        return dict(sorted(resource_counts.items(), key=lambda x: x[1], reverse=True))
    
    def get_sql_resources(self) -> Dict[str, Any]:
        """Extract all SQL servers and databases"""
        sql_resources = {
            'servers': [],
            'databases': []
        }
        
        for rg in self.get_resource_groups():
            rg_name = rg.get('resourceGroupName', 'Unknown')
            sql_data = rg.get('resources', {}).get('sql', {})
            
            for server in sql_data.get('servers', []):
                sql_resources['servers'].append({
                    'name': server.get('name'),
                    'resourceGroup': rg_name,
                    'location': server.get('location'),
                    'administrator_login': server.get('administrator_login'),
                    'state': server.get('state'),
                    'fully_qualified_domain_name': server.get('fully_qualified_domain_name')
                })
            
            for db in sql_data.get('databases', []):
                sql_resources['databases'].append({
                    'name': db.get('name'),
                    'resourceGroup': rg_name,
                    'location': db.get('location'),
                    'status': db.get('status'),
                    'collation': db.get('collation'),
                    'max_size_bytes': db.get('max_size_bytes')
                })
        
        return sql_resources
    
    def get_storage_accounts(self) -> List[Dict[str, Any]]:
        """Extract all storage accounts"""
        storage_accounts = []
        
        for rg in self.get_resource_groups():
            rg_name = rg.get('resourceGroupName', 'Unknown')
            storage_data = rg.get('resources', {}).get('storage', {})
            
            for account in storage_data.get('storageAccounts', []):
                storage_accounts.append({
                    'name': account.get('name'),
                    'resourceGroup': rg_name,
                    'location': account.get('location'),
                    'kind': account.get('kind'),
                    'access_tier': account.get('access_tier'),
                    'enable_https_traffic_only': account.get('enable_https_traffic_only'),
                    'allow_blob_public_access': account.get('allow_blob_public_access')
                })
        
        return storage_accounts
    
    def get_virtual_machines(self) -> List[Dict[str, Any]]:
        """Extract all virtual machines"""
        vms = []
        
        for rg in self.get_resource_groups():
            rg_name = rg.get('resourceGroupName', 'Unknown')
            compute_data = rg.get('resources', {}).get('compute', {})
            
            for vm in compute_data.get('virtualMachines', []):
                vms.append({
                    'name': vm.get('name'),
                    'resourceGroup': rg_name,
                    'location': vm.get('location'),
                    'vm_size': vm.get('hardware_profile', {}).get('vm_size'),
                    'provisioning_state': vm.get('provisioning_state')
                })
        
        return vms
    
    def get_managed_identities(self) -> List[Dict[str, Any]]:
        """Extract all managed identities"""
        identities = []
        
        for rg in self.get_resource_groups():
            rg_name = rg.get('resourceGroupName', 'Unknown')
            identity_data = rg.get('resources', {}).get('managedidentity', {})
            
            for identity in identity_data.get('userAssignedIdentities', []):
                identities.append({
                    'name': identity.get('name'),
                    'resourceGroup': rg_name,
                    'location': identity.get('location'),
                    'principal_id': identity.get('principal_id'),
                    'client_id': identity.get('client_id'),
                    'tenant_id': identity.get('tenant_id')
                })
        
        return identities
    
    def get_data_factories(self) -> List[Dict[str, Any]]:
        """Extract all data factories"""
        adf_list = []
        
        for rg in self.get_resource_groups():
            rg_name = rg.get('resourceGroupName', 'Unknown')
            adf_data = rg.get('resources', {}).get('datafactory', {})
            
            for adf in adf_data.get('dataFactories', []):
                adf_list.append({
                    'name': adf.get('name'),
                    'resourceGroup': rg_name,
                    'location': adf.get('location'),
                    'provisioning_state': adf.get('provisioning_state'),
                    'version': adf.get('version')
                })
        
        return adf_list
    
    def generate_summary_report(self) -> str:
        """Generate a summary report of the infrastructure"""
        report = []
        report.append("=" * 80)
        report.append("AZURE INFRASTRUCTURE SUMMARY REPORT")
        report.append("=" * 80)
        report.append("")
        
        # Subscription Summary
        subscriptions = self.get_subscriptions()
        report.append(f"Total Subscriptions: {len(subscriptions)}")
        for sub in subscriptions:
            report.append(f"  - {sub.get('displayName')} ({sub.get('subscriptionId')})")
        report.append("")
        
        # Resource Groups Summary
        rgs = self.get_resource_groups()
        report.append(f"Total Resource Groups: {len(rgs)}")
        for rg in rgs:
            report.append(f"  - {rg.get('resourceGroupName')}")
        report.append("")
        
        # Resources by Type
        report.append("RESOURCES BY TYPE:")
        report.append("-" * 80)
        resource_counts = self.count_resources_by_type()
        total_resources = sum(resource_counts.values())
        report.append(f"Total Resources: {total_resources}")
        report.append("")
        for resource_type, count in resource_counts.items():
            if count > 0:
                report.append(f"  {resource_type}: {count}")
        report.append("")
        
        # SQL Resources
        sql_resources = self.get_sql_resources()
        if sql_resources['servers'] or sql_resources['databases']:
            report.append("SQL RESOURCES:")
            report.append("-" * 80)
            report.append(f"SQL Servers: {len(sql_resources['servers'])}")
            for server in sql_resources['servers']:
                report.append(f"  - {server['name']} (RG: {server['resourceGroup']})")
            report.append("")
            report.append(f"Databases: {len(sql_resources['databases'])}")
            for db in sql_resources['databases']:
                report.append(f"  - {db['name']} (Status: {db['status']})")
            report.append("")
        
        # Storage Accounts
        storage_accounts = self.get_storage_accounts()
        if storage_accounts:
            report.append("STORAGE ACCOUNTS:")
            report.append("-" * 80)
            report.append(f"Total Storage Accounts: {len(storage_accounts)}")
            for account in storage_accounts:
                report.append(f"  - {account['name']} (Kind: {account['kind']}, Tier: {account['access_tier']})")
            report.append("")
        
        # Virtual Machines
        vms = self.get_virtual_machines()
        if vms:
            report.append("VIRTUAL MACHINES:")
            report.append("-" * 80)
            report.append(f"Total VMs: {len(vms)}")
            for vm in vms:
                report.append(f"  - {vm['name']} ({vm['vm_size']})")
            report.append("")
        
        # Managed Identities
        identities = self.get_managed_identities()
        if identities:
            report.append("MANAGED IDENTITIES:")
            report.append("-" * 80)
            report.append(f"Total User Assigned Identities: {len(identities)}")
            for identity in identities:
                report.append(f"  - {identity['name']}")
            report.append("")
        
        # Data Factories
        data_factories = self.get_data_factories()
        if data_factories:
            report.append("DATA FACTORIES:")
            report.append("-" * 80)
            report.append(f"Total Data Factories: {len(data_factories)}")
            for adf in data_factories:
                report.append(f"  - {adf['name']} (State: {adf['provisioning_state']})")
            report.append("")
        
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def save_report(self, output_file: str) -> None:
        """Save the summary report to a file"""
        report = self.generate_summary_report()
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✓ Report saved to {output_file}")
    
    def export_sql_resources_to_json(self, output_file: str) -> None:
        """Export SQL resources to JSON"""
        sql_resources = self.get_sql_resources()
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sql_resources, f, indent=2)
        print(f"✓ SQL resources exported to {output_file}")
    
    def export_storage_to_json(self, output_file: str) -> None:
        """Export storage accounts to JSON"""
        storage_accounts = self.get_storage_accounts()
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(storage_accounts, f, indent=2)
        print(f"✓ Storage accounts exported to {output_file}")
    
    def export_vms_to_json(self, output_file: str) -> None:
        """Export virtual machines to JSON"""
        vms = self.get_virtual_machines()
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(vms, f, indent=2)
        print(f"✓ Virtual machines exported to {output_file}")


def main():
    """Main function"""
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    json_file = script_dir / 'azure-infraestructure.json'
    
    if not json_file.exists():
        print(f"✗ File not found: {json_file}")
        return
    
    # Initialize the analyzer
    analyzer = AzureInfrastructureAnalyzer(str(json_file))
    
    # Generate and print summary report
    print("\n")
    print(analyzer.generate_summary_report())
    
    # Save reports to files
    output_dir = script_dir / 'reports'
    output_dir.mkdir(exist_ok=True)
    
    analyzer.save_report(str(output_dir / 'infrastructure_summary.txt'))
    analyzer.export_sql_resources_to_json(str(output_dir / 'sql_resources.json'))
    analyzer.export_storage_to_json(str(output_dir / 'storage_accounts.json'))
    analyzer.export_vms_to_json(str(output_dir / 'virtual_machines.json'))
    
    print(f"\n✓ All reports have been generated in: {output_dir}")


if __name__ == "__main__":
    main()
