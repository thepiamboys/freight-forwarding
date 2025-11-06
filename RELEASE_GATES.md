# Release Gates Verification Checklist

This document provides a comprehensive checklist to verify all features before release.

## Gate 1: No Core Modification ✅

- [ ] Verify no files modified in `frappe/` or `erpnext/` directories
- [ ] Verify all customizations are in `freight_forwarding/` app only
- [ ] Verify no core doctype classes overridden (except via hooks)
- [ ] Verify all customizations use standard Frappe hooks and APIs

**Verification:**
```bash
# Check for core modifications
find . -path "./frappe/*" -o -path "./erpnext/*" | grep -v ".git" | wc -l
# Should only show standard files, no custom modifications
```

## Gate 2: Dynamic Naming Active ✅

- [ ] **Project**: Create new Project → verify naming format `{DIV}-{MODE}-{YYYYMMDD}-{###}`
  - Test: Create Project with division="Import", mode="Sea" → should be "IMP-SEA-YYYYMMDD-001"
- [ ] **Sales Invoice**: Create SI with Project → verify naming `{DIV}-SINV-{YYYY}-{#####}`
- [ ] **Purchase Invoice**: Create PI with Project → verify naming `{DIV}-PINV-{YYYY}-{#####}`
- [ ] **Purchase Order**: Create PO with Project → verify naming `{DIV}-PO-{YYYY}-{#####}`
- [ ] **Employee Advance**: Create EADV with Project → verify naming `{DIV}-EADV-{YYYY}-{#####}`
- [ ] **Expense Claim**: Create EC with Project → verify naming `{DIV}-EC-{YYYY}-{#####}`

**Verification:**
```python
# In Frappe console
# Create test documents and verify naming patterns
```

## Gate 3: Division Access (User Permission + PQC) Enforced ✅

- [ ] Create test user with User Permission for Division="Import" only
- [ ] Login as test user → verify can only see Projects with division="Import"
- [ ] Verify PQC active on: Project, Sales Invoice, Purchase Invoice, Purchase Order, Employee Advance, Expense Claim, Payment Entry
- [ ] Verify user cannot access documents from other divisions
- [ ] Verify System Manager can see all documents

**Verification:**
```python
# Test PQC
frappe.set_user("test_user")
projects = frappe.get_list("Project")
# Should only return projects with division="Import"
```

## Gate 4: Project Validations ✅

- [ ] **Sea Mode**: Create Project with mode="Sea" → verify POL/POD required
- [ ] **Air Mode**: Create Project with mode="Air" → verify AOO/AOD required
- [ ] **ETD < ETA**: Create Project with ETD > ETA → verify validation error
- [ ] **Submit**: Try to submit Project without required fields → verify error

**Verification:**
```python
# Test validations
project = frappe.get_doc({
    "doctype": "Project",
    "project_name": "Test",
    "division": "Import",
    "mode": "Sea"
})
project.insert()
# Should fail without POL/POD
```

## Gate 5: Item Group Tree + Default Accounts Ready ✅

- [ ] Verify Item Group "Freight Services" exists
- [ ] Verify child groups: Freight, Customs, Trucking, Port, Warehouse, Surcharges
- [ ] Verify default revenue accounts exist (or can be created)
- [ ] Verify default cost accounts exist (or can be created)
- [ ] Verify accounts linked to Item Groups (if configured)

**Verification:**
```python
# Check Item Groups
frappe.get_all("Item Group", filters={"parent_item_group": "Freight Services"})
# Check Accounts
frappe.get_all("Account", filters={"account_name": ["like", "%Freight%"]})
```

## Gate 6: Sales Tax Rule 1.1% Active; Purchase PPh23 via TWC ✅

- [ ] **Sales Tax**: Create Sales Invoice with item from "Freight Services" → verify 1.1% tax applied
- [ ] **Tax Rule**: Verify Tax Rule "PPN JPT 1,1% - Freight Services" exists and active
- [ ] **Purchase Tax**: Verify Purchase Taxes Template "PPN Masukan" exists
- [ ] **PPh 23**: Verify Tax Withholding Category "PPh 23" exists
- [ ] Test: Create PI with supplier that has TWC → verify PPh 23 applied

**Verification:**
```python
# Create SI with Freight Services item
si = frappe.get_doc({
    "doctype": "Sales Invoice",
    "customer": "Test Customer",
    "project": "test-project",
    "items": [{"item_code": "freight-item", "qty": 1, "rate": 1000}]
})
si.insert()
# Check taxes
print(si.taxes)
# Should show 1.1% tax
```

## Gate 7: Advance Line Working ✅

- [ ] Create Employee Advance with project
- [ ] Add Advance Lines → verify sum(allocated_amount) == advance_amount
- [ ] Try to save with sum != advance_amount → verify validation error
- [ ] Create Expense Claim with advance_line_ref → verify consumption
- [ ] Verify balance_amount = allocated - consumed
- [ ] Verify line_status = "Closed" when balance = 0

**Verification:**
```python
# Create Employee Advance
advance = frappe.get_doc({
    "doctype": "Employee Advance",
    "employee": "test-employee",
    "project": "test-project",
    "advance_amount": 1000,
    "advance_lines": [
        {"project": "test-project", "item": "item1", "service_type": "Freight", "allocated_amount": 600},
        {"project": "test-project", "item": "item2", "service_type": "Customs", "allocated_amount": 400}
    ]
})
advance.insert()
# Verify sum = advance_amount
```

## Gate 8: EC Rows Have project+service_type; Consumption Validated ✅

- [ ] Create Expense Claim → verify each row requires project
- [ ] Verify each row requires service_type
- [ ] Create EC with advance_line_ref → verify consumption works
- [ ] Try to consume more than balance → verify validation error
- [ ] Verify auto-pick advance_line when advance_ref set
- [ ] Verify division auto-set from Project

**Verification:**
```python
# Create Expense Claim
ec = frappe.get_doc({
    "doctype": "Expense Claim",
    "employee": "test-employee",
    "expenses": [
        {
            "expense_type": "Port Handling",
            "amount": 500,
            "project": "test-project",
            "service_type": "Port"
        }
    ]
})
ec.insert()
# Verify project and service_type required
```

## Gate 9: PO/PI/SI Valid; Reports OK ✅

- [ ] **Purchase Order**: Create PO → verify project required, division auto-set
- [ ] **Purchase Invoice**: Create PI → verify project required, division auto-set, classification valid
- [ ] **Sales Invoice**: Create SI → verify project required, division auto-set, 1.1% tax applied
- [ ] **Reports**: Run all 5 reports → verify no errors, data displays correctly
  - Project Service Breakdown
  - Expense Claim Breakdown
  - Advance Utilization
  - PO Commit vs Actual
  - Project Financial Snapshot

**Verification:**
```python
# Test reports
from freight_forwarding.report.project_service_breakdown.project_service_breakdown import execute
columns, data = execute({"project": "test-project"})
print(columns, data)
```

## Gate 10: Project UI (Dashboard Override + Tab Finance Embeds) ✅

- [ ] Open Project form → verify dashboard shows sections: Sales, Purchases, Expenses, Cash & Bank
- [ ] Verify Tab Finance exists
- [ ] Verify lists display: Employee Advances, Expense Claims, Purchase Orders, Purchase Invoices, Sales Invoices, Payments
- [ ] Click "New" buttons → verify project pre-filled
- [ ] Click "View All" links → verify filtered list opens
- [ ] Click on list items → verify document opens

**Verification:**
- Manual UI testing required
- Open Project in browser and verify all UI elements

## Gate 11: Tests Green; Coverage ≥ 60%; Fixtures Exported ✅

- [ ] Run unit tests → verify all pass
- [ ] Run integration tests → verify all pass
- [ ] Check test coverage → verify ≥ 60% (target 80%)
- [ ] Verify fixtures exported:
  - Custom Fields (custom_field.json)
  - Property Setters (property_setter.json)
  - Custom DocTypes (custom_doctype.json)
  - Tax Rule (tax_rule.json)
  - Expense Claim Type (expense_claim_type.json)
  - Roles (role.json)

**Verification:**
```bash
# Run tests
bench --site [site-name] run-tests --app freight_forwarding

# Check coverage
bench --site [site-name] run-tests --coverage

# Verify fixtures
ls freight_forwarding/fixtures/*.json
```

## Additional Verification

### Custom DocTypes
- [ ] FF Port: Create port → verify port_code unique, validation works
- [ ] FF Airport: Create airport → verify iata unique, validation works
- [ ] Advance Line: Verify child table works in Employee Advance

### Client Scripts
- [ ] Verify auto-fill division from Project works on all financial documents
- [ ] Verify auto-set service_type from Item Group works on items
- [ ] Verify Quotation validation for Freight Services items

### Server Scripts
- [ ] Verify all naming series work correctly
- [ ] Verify all validations work correctly
- [ ] Verify expense claim consumption logic works
- [ ] Verify advance line balance calculation works

### API
- [ ] Test list_by_project API → verify returns filtered documents
- [ ] Test import_ports_bootstrap API → verify imports ports
- [ ] Test import_airports_bootstrap API → verify imports airports

### Workflows
- [ ] Create Opportunity → set Won → verify Project auto-created
- [ ] Create Quotation → set Won → verify Project auto-created
- [ ] Verify Project fields copied from Opp/Quotation

## Pre-Release Checklist

- [ ] All gates passed
- [ ] Documentation updated (README.md, INSTALL.md, DEPLOYMENT.md)
- [ ] CHANGELOG.md updated
- [ ] Version number updated in setup.py and manifest.json
- [ ] All fixtures exported and verified
- [ ] Code review completed
- [ ] Security review completed
- [ ] Performance tested
- [ ] Backup procedures documented
- [ ] Rollback procedure tested

## Release Sign-off

- [ ] Development Lead: _________________ Date: _______
- [ ] QA Lead: _________________ Date: _______
- [ ] Product Owner: _________________ Date: _______

---

**Note:** All gates must pass before release. If any gate fails, fix the issue and re-verify.

