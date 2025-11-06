# Data Backfill Scripts

Scripts untuk migrasi data existing ke struktur Freight Forwarding.

## Scripts Available

### 1. backfill_division
Set division pada dokumen yang missing division.

**Usage:**
```python
# Dry run (preview only)
frappe.call("freight_forwarding.utils.backfill.data_backfill.backfill_division", {"dry_run": True})

# Actual update
frappe.call("freight_forwarding.utils.backfill.data_backfill.backfill_division", {"dry_run": False})
```

**What it does:**
- Mencari dokumen tanpa division: Project, Sales Invoice, Purchase Invoice, Purchase Order, Employee Advance, Expense Claim, Payment Entry
- Untuk dokumen dengan project link, ambil division dari Project
- Project tanpa division akan di-skip (harus di-set manual)

### 2. backfill_project_links
Mencari dokumen finansial yang belum di-link ke Project.

**Usage:**
```python
frappe.call("freight_forwarding.utils.backfill.data_backfill.backfill_project_links", {"dry_run": True})
```

**What it does:**
- Mencari dokumen tanpa project: Sales Invoice, Purchase Invoice, Purchase Order, Employee Advance, Payment Entry
- Menampilkan suggestions untuk manual linking
- **Note:** Actual linking harus dilakukan manual berdasarkan business logic

### 3. backfill_expense_claim_project
Set project pada Expense Claim Detail rows yang missing.

**Usage:**
```python
# Dry run
frappe.call("freight_forwarding.utils.backfill.data_backfill.backfill_expense_claim_project", {"dry_run": True})

# Actual update
frappe.call("freight_forwarding.utils.backfill.data_backfill.backfill_expense_claim_project", {"dry_run": False})
```

**What it does:**
- Mencari Expense Claim Detail tanpa project
- Ambil project dari parent Expense Claim jika ada
- Update detail rows

### 4. run_all_backfills
Jalankan semua backfill scripts sekaligus.

**Usage:**
```python
# Dry run
frappe.call("freight_forwarding.utils.backfill.data_backfill.run_all_backfills", {"dry_run": True})

# Actual update
frappe.call("freight_forwarding.utils.backfill.data_backfill.run_all_backfills", {"dry_run": False})
```

## Important Notes

1. **Always run dry_run=True first** untuk preview perubahan
2. **Backup database** sebelum menjalankan actual updates
3. **Project linking** harus dilakukan manual berdasarkan business logic (customer, supplier, dates, etc.)
4. **Division pada Project** harus di-set manual karena tidak ada auto-logic

## Example Usage in Console

```python
# 1. Preview changes
result = frappe.call("freight_forwarding.utils.backfill.data_backfill.run_all_backfills", {"dry_run": True})
print(result)

# 2. If OK, run actual updates
result = frappe.call("freight_forwarding.utils.backfill.data_backfill.run_all_backfills", {"dry_run": False})
print(result)
```

## Migration Checklist

- [ ] Backup database
- [ ] Run dry_run untuk semua scripts
- [ ] Review results
- [ ] Set division pada Projects yang missing (manual)
- [ ] Link financial documents ke Projects (manual, berdasarkan business logic)
- [ ] Run actual backfill untuk division (dari Project)
- [ ] Run actual backfill untuk Expense Claim Detail project
- [ ] Verify results

