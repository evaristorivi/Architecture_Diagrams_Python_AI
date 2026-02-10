"""
Usage examples for Azure Infrastructure Analyzer
"""

from azure_infrastructure_analyzer import AzureInfrastructureAnalyzer
from pathlib import Path
import json


def example_1_basic_summary():
    """Example 1: Generate and print basic summary"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Summary Report")
    print("="*80)
    
    analyzer = AzureInfrastructureAnalyzer('azure-infraestructure.json')
    print(analyzer.generate_summary_report())


def example_2_get_sql_details():
    """Example 2: Extract and display SQL resources"""
    print("\n" + "="*80)
    print("EXAMPLE 2: SQL Resources Details")
    print("="*80)
    
    analyzer = AzureInfrastructureAnalyzer('azure-infraestructure.json')
    sql_resources = analyzer.get_sql_resources()
    
    print(f"\nFound {len(sql_resources['servers'])} SQL Servers:")
    for server in sql_resources['servers']:
        print(f"\n  Server: {server['name']}")
        print(f"    Resource Group: {server['resourceGroup']}")
        print(f"    Location: {server['location']}")
        print(f"    State: {server['state']}")
        print(f"    FQDN: {server['fully_qualified_domain_name']}")
    
    print(f"\n\nFound {len(sql_resources['databases'])} Databases:")
    for db in sql_resources['databases']:
        print(f"\n  Database: {db['name']}")
        print(f"    Resource Group: {db['resourceGroup']}")
        print(f"    Status: {db['status']}")
        print(f"    Max Size: {db['max_size_bytes']} bytes")


def example_3_storage_accounts():
    """Example 3: Get storage account details"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Storage Accounts")
    print("="*80)
    
    analyzer = AzureInfrastructureAnalyzer('azure-infraestructure.json')
    storage_accounts = analyzer.get_storage_accounts()
    
    print(f"\nFound {len(storage_accounts)} Storage Accounts:")
    for account in storage_accounts:
        print(f"\n  Name: {account['name']}")
        print(f"    Resource Group: {account['resourceGroup']}")
        print(f"    Location: {account['location']}")
        print(f"    Kind: {account['kind']}")
        print(f"    Access Tier: {account['access_tier']}")
        print(f"    HTTPS Only: {account['enable_https_traffic_only']}")
        print(f"    Public Access: {account['allow_blob_public_access']}")


def example_4_resource_counts():
    """Example 4: Count resources by type"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Resource Type Summary")
    print("="*80)
    
    analyzer = AzureInfrastructureAnalyzer('azure-infraestructure.json')
    resource_counts = analyzer.count_resources_by_type()
    
    print("\nResources by Type:")
    total = 0
    for resource_type, count in resource_counts.items():
        if count > 0:
            print(f"  {resource_type}: {count}")
            total += count
    print(f"\nTotal Resources: {total}")


def example_5_resource_groups():
    """Example 5: List all resource groups"""
    print("\n" + "="*80)
    print("EXAMPLE 5: Resource Groups")
    print("="*80)
    
    analyzer = AzureInfrastructureAnalyzer('azure-infraestructure.json')
    resource_groups = analyzer.get_resource_groups()
    
    print(f"\nFound {len(resource_groups)} Resource Groups:")
    for rg in resource_groups:
        tags = rg.get('tags', {})
        print(f"\n  Name: {rg['resourceGroupName']}")
        print(f"    ID: {rg['resourceGroupId']}")
        if tags:
            print(f"    Tags: {tags}")


def example_6_subscriptions():
    """Example 6: List subscriptions"""
    print("\n" + "="*80)
    print("EXAMPLE 6: Subscriptions")
    print("="*80)
    
    analyzer = AzureInfrastructureAnalyzer('azure-infraestructure.json')
    subscriptions = analyzer.get_subscriptions()
    
    print(f"\nFound {len(subscriptions)} Subscription(s):")
    for sub in subscriptions:
        print(f"\n  Name: {sub['displayName']}")
        print(f"    Subscription ID: {sub['subscriptionId']}")
        print(f"    Resource Groups: {len(sub.get('resourceGroups', []))}")


def example_7_managed_identities():
    """Example 7: List managed identities"""
    print("\n" + "="*80)
    print("EXAMPLE 7: Managed Identities")
    print("="*80)
    
    analyzer = AzureInfrastructureAnalyzer('azure-infraestructure.json')
    identities = analyzer.get_managed_identities()
    
    print(f"\nFound {len(identities)} Managed Identity/Identities:")
    for identity in identities:
        print(f"\n  Name: {identity['name']}")
        print(f"    Resource Group: {identity['resourceGroup']}")
        print(f"    Location: {identity['location']}")
        print(f"    Principal ID: {identity['principal_id']}")
        print(f"    Client ID: {identity['client_id']}")


def example_8_virtual_machines():
    """Example 8: List virtual machines"""
    print("\n" + "="*80)
    print("EXAMPLE 8: Virtual Machines")
    print("="*80)
    
    analyzer = AzureInfrastructureAnalyzer('azure-infraestructure.json')
    vms = analyzer.get_virtual_machines()
    
    print(f"\nFound {len(vms)} Virtual Machine(s):")
    for vm in vms:
        print(f"\n  Name: {vm['name']}")
        print(f"    Resource Group: {vm['resourceGroup']}")
        print(f"    Location: {vm['location']}")
        print(f"    Size: {vm['vm_size']}")
        print(f"    State: {vm['provisioning_state']}")


def example_9_data_factories():
    """Example 9: List data factories"""
    print("\n" + "="*80)
    print("EXAMPLE 9: Data Factories")
    print("="*80)
    
    analyzer = AzureInfrastructureAnalyzer('azure-infraestructure.json')
    data_factories = analyzer.get_data_factories()
    
    print(f"\nFound {len(data_factories)} Data Factory/Factories:")
    for adf in data_factories:
        print(f"\n  Name: {adf['name']}")
        print(f"    Resource Group: {adf['resourceGroup']}")
        print(f"    Location: {adf['location']}")
        print(f"    Version: {adf['version']}")
        print(f"    State: {adf['provisioning_state']}")


def example_10_export_reports():
    """Example 10: Export multiple reports"""
    print("\n" + "="*80)
    print("EXAMPLE 10: Export Reports to Files")
    print("="*80)
    
    analyzer = AzureInfrastructureAnalyzer('azure-infraestructure.json')
    
    # Create reports directory
    reports_dir = Path('./reports')
    reports_dir.mkdir(exist_ok=True)
    
    # Save various reports
    analyzer.save_report(str(reports_dir / 'infrastructure_summary.txt'))
    analyzer.export_sql_resources_to_json(str(reports_dir / 'sql_resources.json'))
    analyzer.export_storage_to_json(str(reports_dir / 'storage_accounts.json'))
    analyzer.export_vms_to_json(str(reports_dir / 'virtual_machines.json'))
    
    print(f"\nReports exported to: {reports_dir}")


if __name__ == "__main__":
    """Run all examples"""
    try:
        # Uncomment the examples you want to run
        
        example_1_basic_summary()
        example_2_get_sql_details()
        example_3_storage_accounts()
        example_4_resource_counts()
        example_5_resource_groups()
        example_6_subscriptions()
        example_7_managed_identities()
        example_8_virtual_machines()
        example_9_data_factories()
        example_10_export_reports()
        
        print("\n" + "="*80)
        print("All examples completed successfully!")
        print("="*80)
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
