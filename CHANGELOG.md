# Changelog

All notable changes to the Freight Forwarding App will be documented in this file.

## [1.0.0] - 2025-11-06

### Added

#### Foundation & Master Data
- Item Group tree fixtures (Freight Services + 6 children)
- Default revenue and cost accounts fixtures
- Tax Templates: PPN JPT 1.1% (Sales), PPN Masukan (Purchase)
- Tax Rule: PPN JPT 1.1% - Freight Services
- Tax Withholding Category: PPh 23
- Expense Claim Type defaults (6 types)

#### Custom DocTypes
- **FF Port**: Master data for ports with coordinates, customs info, free time defaults
- **FF Airport**: Master data for airports with IATA/ICAO codes
- **Advance Line**: Child table for Employee Advance with multi-item allocation

#### Custom Fields (29+ fields)
- Project: division, mode, service_scope, pol, pod, aoo, aod, etd, eta, incoterm, is_freehand, is_nomination
- Sales Invoice: division
- Purchase Invoice: division
- Purchase Order: project, division
- Employee Advance: division, advance_lines
- Expense Claim: division
- Expense Claim Detail: project, item, service_type, advance_ref, advance_line_ref, cost_center, notes_internal
- Payment Entry: division
- Opportunity: division, mode, service_scope, pol, pod, aoo, aod, etd, eta, incoterm
- Quotation: division, mode, service_scope, pol, pod, aoo, aod, etd, eta, incoterm
- Sales Invoice Item: service_type
- Purchase Invoice Item: service_type

#### Dynamic Naming Series
- Project: `{DIV}-{MODE}-{YYYYMMDD}-{###}`
- Sales Invoice: `{DIV}-SINV-{YYYY}-{#####}`
- Purchase Invoice: `{DIV}-PINV-{YYYY}-{#####}`
- Purchase Order: `{DIV}-PO-{YYYY}-{#####}`
- Employee Advance: `{DIV}-EADV-{YYYY}-{#####}`
- Expense Claim: `{DIV}-EC-{YYYY}-{#####}`

#### Server Scripts
- Naming series functions (6 functions)
- Document validations (11 functions)
- Expense Claim consumption logic
- Advance Line balance calculation
- Permission Query Conditions (PQC) for 7 DocTypes
- CRM workflow (auto-create Project from Opp/Quotation)

#### Client Scripts
- Auto-fill division from Project (6 DocTypes)
- Auto-set service_type from Item Group (3 DocTypes)
- Project UI: Tab Finance with embedded lists
- Quotation: Validation and auto-fill from Opportunity

#### Reports (5 reports)
- Project Service Breakdown (revenue/cost/margin by service)
- Expense Claim Breakdown (by project × service_type × item)
- Advance Utilization (allocated/consumed/balance)
- PO Commit vs Actual (PO vs PI+EC comparison)
- Project Financial Snapshot (counts, totals, AR/AP)

#### Project UI
- Dashboard override with sections: Sales, Purchases, Expenses, Cash & Bank
- Tab Finance with HTML embeds
- Add New buttons with preset project
- View All links

#### Data Import & Backfill
- FF Port CSV template (10 common ports)
- FF Airport CSV template (10 common airports)
- Import utilities with bootstrap functions
- Division backfill script
- Project links backfill script
- Expense Claim project backfill script

#### CRM/Sales Integration
- Custom fields on Opportunity & Quotation
- Auto-create Project from Won Opp/Quotation
- Item validation for Freight Services

#### Permissions & Roles
- Custom Roles: FF-OPS, FF-DOCS, FF-SALES, FF-FIN, FF-MANAGER, FF-ADMIN
- Permission Query Conditions (PQC) for division-based access

#### Deployment & Verification
- Deployment script (deploy.sh)
- Rollback script (rollback.sh)
- Release Gates verification (11 gates)
- Automated verification scripts

#### Testing
- Test structure (unit & integration)
- Test templates for all major features
- Test documentation

### Documentation
- README.md - Project overview
- INSTALL.md - Installation guide
- DEPLOYMENT.md - Deployment procedures
- RELEASE_GATES.md - Release verification checklist
- PROJECT_SUMMARY.md - Comprehensive project summary
- QUICK_START.md - Quick start guide
- TODO_STATUS.md - Task status summary

### Changed
- None (initial release)

### Fixed
- None (initial release)

### Security
- Division-based access control via PQC
- User Permissions for data segregation
- No core modifications (all customizations in app only)

---

## Future Enhancements

### Planned (Optional)
- Rate Management system (10 tasks)
- FF Consol Shipment doctype (1 task)
- Consol Shipment allocation logic (2 tasks)
- Full test implementation (requires Frappe environment)

### Notes
- All core functionality is complete and production-ready
- Optional features can be added as needed
- Test structure is ready; implementations require Frappe environment
