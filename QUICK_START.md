# Quick Start Guide

Panduan cepat untuk memulai menggunakan Freight Forwarding App.

## 🚀 Installation

### 1. Install App

```bash
# Dari bench directory
cd /path/to/your/bench
bench get-app freight_forwarding /Users/mac/Desktop/DEV/Freightforwading
bench --site [your-site-name] install-app freight_forwarding
```

### 2. Migrate (Import Fixtures)

```bash
bench --site [your-site-name] migrate
```

Ini akan mengimport:
- Custom Fields
- Property Setters
- Custom DocTypes (FF Port, FF Airport, Advance Line)
- Tax Rule (PPN JPT 1.1%)
- Expense Claim Types
- Roles (FF-OPS, FF-DOCS, FF-SALES, FF-FIN, FF-MANAGER, FF-ADMIN)

### 3. Build Assets

```bash
bench build --app freight_forwarding
bench restart
```

## 📋 Initial Setup Checklist

### Step 1: Master Data Setup

- [ ] **Item Groups**: Import atau create Item Group tree
  - Root: "Freight Services"
  - Children: Freight, Customs, Trucking, Port, Warehouse, Surcharges
  
  ```python
  # Via console atau Data Import
  # File: freight_forwarding/fixtures/item_group.json
  ```

- [ ] **Accounts**: Create default accounts (atau import dari fixtures)
  - Revenue: Freight Revenue, Customs Service Revenue, Trucking Revenue, Port Service Revenue, Warehouse Service Revenue, Surcharges Revenue
  - Cost: Freight Cost, Customs Service Cost, Trucking Cost, Port Service Cost, Warehouse Service Cost, Surcharges Cost
  
  ```python
  # File: freight_forwarding/fixtures/accounts.json
  # Note: Adjust parent accounts sesuai Chart of Accounts Anda
  ```

- [ ] **Tax Templates**: Import atau create
  - Sales: "PPN JPT 1,1%" (1.1% on Net Total)
  - Purchase: "PPN Masukan" (11% on Net Total)
  
  ```python
  # File: freight_forwarding/fixtures/tax_template.json
  ```

- [ ] **Tax Rule**: Import
  - "PPN JPT 1,1% - Freight Services"
  
  ```python
  # File: freight_forwarding/fixtures/tax_rule.json
  ```

- [ ] **Tax Withholding Category**: Import
  - "PPh 23" (2%)
  
  ```python
  # File: freight_forwarding/fixtures/tax_withholding_category.json
  ```

### Step 2: Master Data Import (Optional)

- [ ] **FF Port**: Import common ports
  
  ```python
  bench --site [site-name] console
  >>> from freight_forwarding.utils.import_data import import_ports_bootstrap
  >>> import_ports_bootstrap()
  ```

- [ ] **FF Airport**: Import common airports
  
  ```python
  >>> from freight_forwarding.utils.import_data import import_airports_bootstrap
  >>> import_airports_bootstrap()
  ```

### Step 3: User Setup

- [ ] **Create Users** dan assign roles:
  - FF-OPS (Operations)
  - FF-DOCS (Documentation)
  - FF-SALES (Sales)
  - FF-FIN (Finance)
  - FF-MANAGER (Manager)
  - FF-ADMIN (Administrator)

- [ ] **Set User Permissions** untuk Division access:
  - Setup → Users → [User] → Permissions
  - Add User Permission: For "Division", Allow "Import" (contoh)
  - User hanya bisa akses documents dengan division yang diizinkan

### Step 4: Data Migration (Jika ada existing data)

- [ ] **Run Backfill Scripts**:
  
  ```python
  bench --site [site-name] console
  >>> from freight_forwarding.utils.backfill.data_backfill import run_all_backfills
  >>> result = run_all_backfills(dry_run=True)  # Preview
  >>> print(result)
  >>> # Review results, then:
  >>> run_all_backfills(dry_run=False)  # Execute
  ```

## 🎯 First Project Workflow

### 1. Create Project

1. Go to **Project** → New
2. Fill required fields:
   - **Project Name**: e.g., "Import Jakarta-Singapore"
   - **Division**: Select (Export/Import/Domestic/Project)
   - **Mode**: MultiSelect (Sea/Air/Land)
   - **Service Scope**: MultiSelect (Freight/Customs/Trucking/Port/Warehouse/Surcharges)
   - **POL/POD** (if Sea): Select FF Port
   - **AOO/AOD** (if Air): Select FF Airport
   - **ETD/ETA**: Set dates
   - **Incoterm**: e.g., "FOB", "CIF"
3. Save → Project akan auto-named: `{DIV}-{MODE}-{YYYYMMDD}-{###}`

### 2. Create Sales Invoice

1. Go to **Sales Invoice** → New
2. Select **Customer**
3. Select **Project** → Division akan auto-filled
4. Add Items (harus dari "Freight Services" subtree)
5. Save → SI akan auto-named: `{DIV}-SINV-{YYYY}-{#####}`
6. Submit → Tax 1.1% akan auto-applied

### 3. Create Purchase Order

1. Go to **Purchase Order** → New
2. Select **Supplier**
3. Select **Project** → Division akan auto-filled
4. Add Items
5. Save → PO akan auto-named: `{DIV}-PO-{YYYY}-{#####}`

### 4. Create Employee Advance

1. Go to **Employee Advance** → New
2. Select **Employee**
3. Select **Project** → Division akan auto-filled
4. Set **Advance Amount**
5. Add **Advance Lines**:
   - Project (same as header)
   - Item
   - Service Type
   - Allocated Amount
   - Notes (optional)
6. Verify: Sum of Allocated Amount = Advance Amount
7. Save → EADV akan auto-named: `{DIV}-EADV-{YYYY}-{#####}`

### 5. Create Expense Claim

1. Go to **Expense Claim** → New
2. Select **Employee**
3. Add **Expenses**:
   - Expense Type
   - Amount
   - **Project** (required)
   - **Service Type** (required)
   - **Advance Reference** (optional)
   - **Advance Line Reference** (optional - auto-picked if advance_ref set)
4. Save → EC akan auto-named: `{DIV}-EC-{YYYY}-{#####}`
5. Submit → Advance Line akan auto-consumed

## 📊 View Reports

1. **Project Service Breakdown**
   - Go to Reports → Project Service Breakdown
   - Filter by Project
   - View revenue/cost/margin by service category

2. **Expense Claim Breakdown**
   - Go to Reports → Expense Claim Breakdown
   - Filter by Project, Service Type, Date Range
   - View sum by project × service_type × item

3. **Advance Utilization**
   - Go to Reports → Advance Utilization
   - Filter by Project, Advance, Service Type
   - View allocated/consumed/balance

4. **PO Commit vs Actual**
   - Go to Reports → PO Commit vs Actual
   - Compare PO committed vs PI + EC actual

5. **Project Financial Snapshot**
   - Go to Reports → Project Financial Snapshot
   - View counts, totals, AR/AP outstanding per project

## 🔍 Verify Installation

Run release gates verification:

```python
bench --site [site-name] console
>>> from freight_forwarding.utils.verification.release_gates import run_all_gates
>>> result = run_all_gates()
>>> print(result)
```

All gates should pass before production use.

## 🆘 Troubleshooting

### Custom Fields Not Showing

```bash
# Rebuild assets
bench build --app freight_forwarding
bench restart

# Clear cache
bench --site [site-name] clear-cache
```

### Naming Not Working

- Verify hooks.py is correct
- Check server scripts are in place
- Verify Project has division and mode set

### Tax Not Applied

- Verify Tax Rule exists and is active
- Check Item Group is under "Freight Services"
- Verify Tax Template is configured correctly

### PQC Not Working

- Verify User Permissions are set
- Check permission_query.py functions exist
- Verify hooks.py has PQC registered

## 📚 Additional Resources

- **README.md**: Project overview
- **INSTALL.md**: Detailed installation guide
- **DEPLOYMENT.md**: Deployment procedures
- **RELEASE_GATES.md**: Verification checklist
- **PROJECT_SUMMARY.md**: Complete project summary

## ✅ Production Readiness Checklist

- [ ] All fixtures imported
- [ ] Item Groups configured
- [ ] Accounts created
- [ ] Tax Templates configured
- [ ] Tax Rule active
- [ ] Users created with roles
- [ ] User Permissions set for Division access
- [ ] Master data imported (Ports/Airports)
- [ ] Backfill scripts run (if migrating)
- [ ] Release gates verified
- [ ] Test workflow: Project → SI → PO → EADV → EC
- [ ] Reports tested
- [ ] UI tested (Project dashboard & Tab Finance)

---

**Ready to go!** 🚀

