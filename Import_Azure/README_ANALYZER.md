# Azure Infrastructure Analyzer

A Python script to parse, analyze, and generate reports from Azure infrastructure exported as JSON.

## Overview

This tool analyzes Azure infrastructure data exported from the Azure portal. It extracts and organizes information about:

- **Subscriptions**: Lists all Azure subscriptions
- **Resource Groups**: Organizes resources by resource groups
- **SQL Resources**: SQL servers and databases
- **Storage Accounts**: Storage account configurations
- **Virtual Machines**: VM details and configurations  
- **Managed Identities**: User-assigned managed identities
- **Data Factories**: Azure Data Factory instances
- **Network Resources**: Virtual networks, security groups, etc.
- **And more**: All Azure resource types in the export

## Files

### Main Script
- **`azure_infrastructure_analyzer.py`** - Main analyzer class with all functionality

### Supporting Files
- **`examples.py`** - 10 practical examples showing how to use the analyzer
- **`requirements_analyzer.txt`** - Dependencies (Python standard library only)

## Requirements

- **Python 3.6+**
- **No external dependencies** - Uses only Python standard library

## Quick Start

### 1. Run the Default Analysis
```bash
python azure_infrastructure_analyzer.py
```

This will:
- Load the JSON file
- Generate a summary report
- Create a `reports/` directory
- Export detailed JSON files for SQL resources, storage accounts, and VMs
- Display the summary in the console

### 2. Run Examples
```bash
python examples.py
```

This runs 10 examples demonstrating different ways to use the analyzer:

1. **Basic Summary Report** - Overall infrastructure overview
2. **SQL Resources Details** - SQL servers and databases
3. **Storage Accounts** - Storage account configurations
4. **Resource Type Summary** - Count of resources by type
5. **Resource Groups** - List all resource groups
6. **Subscriptions** - List all subscriptions
7. **Managed Identities** - User-assigned identities
8. **Virtual Machines** - VM details
9. **Data Factories** - ADF instances
10. **Export Reports** - Generate all report files

## Usage Examples

### Basic Usage
```python
from azure_infrastructure_analyzer import AzureInfrastructureAnalyzer

# Initialize analyzer
analyzer = AzureInfrastructureAnalyzer('azure-infraestructure.json')

# Generate summary report
print(analyzer.generate_summary_report())
```

### Get Specific Resource Types
```python
# Get SQL resources
sql_resources = analyzer.get_sql_resources()
print(f"SQL Servers: {len(sql_resources['servers'])}")
print(f"Databases: {len(sql_resources['databases'])}")

# Get storage accounts
storage = analyzer.get_storage_accounts()
for account in storage:
    print(f"{account['name']} - {account['kind']}")

# Get virtual machines
vms = analyzer.get_virtual_machines()
for vm in vms:
    print(f"{vm['name']} - {vm['vm_size']}")
```

### Export to Files
```python
# Save text summary
analyzer.save_report('infrastructure_summary.txt')

# Export as JSON
analyzer.export_sql_resources_to_json('sql_resources.json')
analyzer.export_storage_to_json('storage_accounts.json')
analyzer.export_vms_to_json('virtual_machines.json')
```

### Count Resources by Type
```python
resource_counts = analyzer.count_resources_by_type()
for resource_type, count in resource_counts.items():
    print(f"{resource_type}: {count}")
```

### Get Resource Groups
```python
# Get all resource groups
rgs = analyzer.get_resource_groups()

# Get resource groups for specific subscription
rgs_for_sub = analyzer.get_resource_groups('subscription-id-here')
```

## Class Methods

### AzureInfrastructureAnalyzer

#### Initialization
```python
analyzer = AzureInfrastructureAnalyzer(json_file_path)
```

#### Data Retrieval Methods
- `get_subscriptions()` - Return all subscriptions
- `get_resource_groups(subscription_id=None)` - Return resource groups
- `get_sql_resources()` - Return SQL servers and databases
- `get_storage_accounts()` - Return storage accounts
- `get_virtual_machines()` - Return VMs
- `get_managed_identities()` - Return managed identities
- `get_data_factories()` - Return data factories
- `count_resources_by_type()` - Count resources by type

#### Report Generation Methods
- `generate_summary_report()` - Generate text summary
- `save_report(output_file)` - Save text report to file
- `export_sql_resources_to_json(output_file)` - Export SQL data as JSON
- `export_storage_to_json(output_file)` - Export storage data as JSON
- `export_vms_to_json(output_file)` - Export VM data as JSON

## Output Examples

### Summary Report Structure
```
================================================================================
AZURE INFRASTRUCTURE SUMMARY REPORT
================================================================================

Total Subscriptions: 1
  - My-Production-Subscription (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)

Total Resource Groups: 11
  - alerts
  - rgintdba
  - rgintglobal
  ...

RESOURCES BY TYPE:
----------------
Total Resources: 47
  sql.servers: 2
  sql.databases: 6
  storage.storageAccounts: 5
  compute.virtualMachines: 2
  ...
```

### Exported JSON Format

**SQL Resources:**
```json
{
  "servers": [
    {
      "name": "srsqlsmametrics",
      "resourceGroup": "rgrintsmametrics",
      "location": "northeurope",
      "administrator_login": "adminBI",
      "state": "Ready",
      "fully_qualified_domain_name": "srsqlsmametrics.database.windows.net"
    }
  ],
  "databases": [...]
}
```

## Key Features

✓ **No external dependencies** - Uses only Python standard library
✓ **Easy to use** - Simple class-based API
✓ **Comprehensive** - Extracts all resource types
✓ **Flexible export** - Save as text or JSON
✓ **Examples included** - 10 working examples
✓ **Well documented** - Detailed docstrings

## Data Structure

The analyzer works with this JSON structure:
```
subscriptions[]
  ├── subscriptionId
  ├── displayName
  └── resourceGroups[]
      ├── resourceGroupName
      ├── resourceGroupId
      ├── tags
      └── resources
          ├── network
          ├── compute
          ├── storage
          ├── sql
          ├── datafactory
          ├── managedidentity
          └── [other resource types...]
```

## Common Tasks

### Task 1: Get all SQL databases and their sizes
```python
analyzer = AzureInfrastructureAnalyzer('azure-infraestructure.json')
sql = analyzer.get_sql_resources()
for db in sql['databases']:
    size_gb = db['max_size_bytes'] / (1024**3)
    print(f"{db['name']}: {size_gb:.2f} GB")
```

### Task 2: Find all production resources
```python
analyzer = AzureInfrastructureAnalyzer('azure-infraestructure.json')
for rg in analyzer.get_resource_groups():
    tags = rg.get('tags', {})
    if tags.get('environment') == 'PRO':
        print(f"Resource Group: {rg['resourceGroupName']}")
```

### Task 3: Generate compliance report
```python
analyzer = AzureInfrastructureAnalyzer('azure-infraestructure.json')
storage = analyzer.get_storage_accounts()

print("Storage Account Security Review:")
for account in storage:
    status = "✓" if account['enable_https_traffic_only'] else "✗"
    print(f"{status} {account['name']}: HTTPS={account['enable_https_traffic_only']}")
```

### Task 4: Resource inventory for cost analysis
```python
analyzer = AzureInfrastructureAnalyzer('azure-infraestructure.json')
counts = analyzer.count_resources_by_type()

print("Resource Inventory for Cost Analysis:")
for resource_type, count in sorted(counts.items()):
    if count > 0:
        print(f"  {resource_type}: {count}")
```

## Troubleshooting

### File not found
Ensure the JSON file is in the same directory as the script or provide the full path:
```python
analyzer = AzureInfrastructureAnalyzer('/path/to/azure-infraestructure.json')
```

### Invalid JSON
Verify the JSON file is valid using a JSON validator

### Empty results
Check that the JSON export includes the resource types you're querying

## Customization

You can extend the analyzer by adding new methods:

```python
class CustomAnalyzer(AzureInfrastructureAnalyzer):
    def get_production_resources(self):
        """Get only production resources"""
        resources = []
        for rg in self.get_resource_groups():
            tags = rg.get('tags', {})
            if tags.get('environment') == 'PRO':
                resources.append(rg)
        return resources
```

## License

This script is provided as-is for analyzing Azure infrastructure exports.

## Support

For issues or questions:
1. Check the examples.py file
2. Review the method docstrings
3. Ensure the JSON file format matches the expected structure
