# Fixtures Directory

This directory contains JSON fixture files for importing master data and configurations.

## Fixture Files

### item_group.json
Item Group tree for Freight Services:
- Freight Services (root)
  - Freight
  - Customs
  - Trucking
  - Port
  - Warehouse
  - Surcharges

### accounts.json
Default revenue and cost accounts:
- Revenue: Freight Revenue, Customs Service Revenue, Trucking Revenue, Port Service Revenue, Warehouse Service Revenue, Surcharges Revenue
- Cost: Freight Cost, Customs Service Cost, Trucking Cost, Port Service Cost, Warehouse Service Cost, Surcharges Cost

**Note:** Parent accounts (Income - FF, Expenses - FF) must exist in your Chart of Accounts before importing.

### tax_template.json
Tax templates:
- **PPN JPT 1,1%** (Sales Taxes Template): On Net Total 1.1%, Account: PPN Keluaran - FF
- **PPN Masukan** (Purchase Taxes Template): On Net Total 11%, Account: PPN Masukan - FF

**Note:** Tax account (PPN Keluaran - FF, PPN Masukan - FF) must exist before importing.

### tax_rule.json
Tax Rule for Freight Services:
- **PPN JPT 1,1% - Freight Services**: Applies Sales Tax Template "PPN JPT 1,1%" to Item Group "Freight Services"

### tax_withholding_category.json
Tax Withholding Category:
- **PPh 23**: Rate 2%, Account: PPh 23 Dipotong - FF

**Note:** Account (PPh 23 Dipotong - FF) must exist before importing.

## Import Instructions

After installing the app, import fixtures:

```bash
bench --site [your-site] import-doc path freight_forwarding/fixtures/item_group.json
bench --site [your-site] import-doc path freight_forwarding/fixtures/accounts.json
```

Or use Frappe's import feature in the UI:
1. Go to Setup → Data → Data Import
2. Select DocType and upload the JSON file

## Important Notes

1. **Account Names**: The fixture files use account names with "- FF" suffix. Adjust according to your Chart of Accounts structure.
2. **Parent Accounts**: Ensure parent accounts (Income - FF, Expenses - FF) exist before importing accounts.
3. **Company**: Accounts are company-agnostic in fixtures. You may need to create company-specific accounts after import.

## Future Fixtures

Additional fixtures will be added:
- Custom Fields (custom_field.json)
- Property Setters (property_setter.json)
- Custom DocTypes (custom_doctype.json)
- Tax Rules (tax_rule.json)
- Expense Claim Types (expense_claim_type.json)

