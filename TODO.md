# TODO List - Freight Forwarding App

Comprehensive development plan based on migration order and requirements.

## Phase 1: Foundation & Master Data Setup

### 1.1 Master Data Setup
- [ ] Create Item Group tree (Freight Services root + children: Freight, Customs, Trucking, Port, Warehouse, Surcharges)
- [ ] Create default revenue accounts (Freight Revenue, Customs Service Revenue, Trucking Revenue, Port Service Revenue, Warehouse Service Revenue, Surcharges Revenue)
- [ ] Create default direct cost accounts (Freight Cost, Customs Service Cost, Trucking Cost, Port Service Cost, Warehouse Service Cost, Surcharges Cost)

### 1.2 Tax Setup
- [ ] Create Sales Taxes Template "PPN JPT 1,1%" (On Net Total 1.1%, Account: PPN Keluaran)
- [ ] Create Tax Rule to apply 1.1% JPT rule to Item Group subtree "Freight Services"
- [ ] Create Purchase Taxes Template (PPN Masukan)
- [ ] Create Tax Withholding Category (PPh 23) for supplier applicable

### 1.3 Expense Claim Types
- [ ] Create Expense Claim Type defaults with account mappings:
  - Port Handling → Port Service Cost
  - Customs Brokerage → Customs Service Cost
  - Trucking OPEX → Trucking Cost
  - Warehouse/Storage → Warehouse Service Cost
  - Surcharges Ops → Surcharges Cost

## Phase 2: Custom Doctypes

### 2.1 Master Data Doctypes
- [ ] **FF Port** (Master)
  - Fields: port_code (UNIQUE), port_name, country (Link Country), city, port_type (Sea/River/Rail/ICD), lat, lon, timezone, has_customs, free_time_default_demurrage, free_time_default_detention
  
- [ ] **FF Airport** (Master)
  - Fields: iata (UNIQUE), icao (optional), airport_name, city, country, lat, lon, timezone, has_customs

### 2.2 Transaction Doctypes
- [ ] **Advance Line** (Custom Child of Employee Advance)
  - Fields: project (Link Project, reqd), item (Link Item, reqd), item_group (RO, autofill), service_type (Select, reqd), allocated_amount (Currency, reqd), consumed_amount (Currency, RO, default 0), balance_amount (Currency, RO), notes (Small Text), line_status (Select: Open/Closed, RO)
  
- [ ] **FF Consol Shipment** (Optional, Recommended)
  - Header: division, mode, mbl_or_mawb_no, carrier_or_airline, vessel_or_flight, pol/pod or aoo/aod, etd, eta
  - Children: consol_member (project, hbl/hawb_no, weight, cbm, chargeable), allocation_rule (charge_code/item, method)

## Phase 3: Custom Fields & Property Setters

### 3.1 Project Custom Fields
- [ ] Add division (Select) field to Project
- [ ] Add mode (MultiSelect) field to Project
- [ ] Add service_scope (MultiSelect) field to Project
- [ ] Add pol (Link FF Port) field to Project
- [ ] Add pod (Link FF Port) field to Project
- [ ] Add aoo (Link FF Airport) field to Project
- [ ] Add aod (Link FF Airport) field to Project
- [ ] Add etd, eta, incoterm, is_freehand, is_nomination fields to Project

### 3.2 Financial Documents Custom Fields
- [ ] Add division field to: Sales Invoice, Purchase Invoice, Purchase Order, Employee Advance, Expense Claim, Payment Entry
- [ ] Add project field to Purchase Order header
- [ ] Add service_type fallback field to Sales Invoice Item
- [ ] Add service_type fallback field to Purchase Invoice Item

### 3.3 Expense Claim Custom Fields
- [ ] Add project (Link Project, reqd) to Expense Claim Detail
- [ ] Add item (Link Item) to Expense Claim Detail
- [ ] Add service_type (Select, reqd) to Expense Claim Detail
- [ ] Add advance_ref (Link Employee Advance) to Expense Claim Detail
- [ ] Add advance_line_ref (Link Advance Line) to Expense Claim Detail
- [ ] Add cost_center (Link Cost Center) to Expense Claim Detail
- [ ] Add notes_internal to Expense Claim Detail

### 3.4 Property Setters
- [ ] Make division field required on Project
- [ ] Make project field required on SI, PI, PO, EADV, EC
- [ ] Set field labels and visibility as needed

## Phase 4: Server Scripts (Naming, Validations, PQC)

### 4.1 Dynamic Naming Series
- [ ] **Project naming** - before_insert: Generate `{DIV}-{MODE}-{YYYYMMDD}-{###}` format
  - Read division + first mode
  - Compose prefix using DIVISION_CODES and MODE_CODES
  - Use make_autoname
  
- [ ] **Sales Invoice naming** - before_insert: Generate `{DIV}-SINV-{YYYY}-{#####}` format
  - Read division from linked Project
  
- [ ] **Purchase Invoice naming** - before_insert: Generate `{DIV}-PINV-{YYYY}-{#####}` format
  
- [ ] **Purchase Order naming** - before_insert: Generate `{DIV}-PO-{YYYY}-{#####}` format
  
- [ ] **Employee Advance naming** - before_insert: Generate `{DIV}-EADV-{YYYY}-{#####}` format
  
- [ ] **Expense Claim naming** - before_insert: Generate `{DIV}-EC-{YYYY}-{#####}` format

### 4.2 Document Validations
- [ ] **Project validation** - before_submit:
  - Sea mode requires POL/POD
  - Air mode requires AOO/AOD
  - ETD < ETA validation
  
- [ ] **Sales Invoice validation** - before_submit:
  - Require project
  - Ensure item classification
  - Ensure 1.1% tax rule applied
  - Set division from Project
  
- [ ] **Purchase Invoice validation** - before_submit:
  - Require project
  - Ensure classification valid
  - Ensure TWC if supplier applicable
  - Set division from Project
  
- [ ] **Purchase Order validation** - before_submit:
  - Require project
  - Ensure service classification
  
- [ ] **Expense Claim validation** - before_submit:
  - Each row must have project & service_type
  - Apply consumption rules
  - Set cost_center (by division mapping) if empty
  - Set division (header) from Project
  
- [ ] **Employee Advance validation** - before_save:
  - sum(allocated_amount) == advance_amount
  - all child.project == header.project

### 4.3 Advance Line Logic
- [ ] **Advance Line balance calculation** - on_update:
  - balance = allocated - consumed
  - Close when balance = 0

### 4.4 Expense Claim Consumption Logic
- [ ] **Consumption with advance_line_ref** - before_submit:
  - If advance_line_ref set → validate project & saldo
  - Consume amount from advance_line
  
- [ ] **Auto-pick matching line** - before_submit:
  - Else if advance_ref set → auto-pick matching line (by item/service_type) with sufficient balance
  - Set advance_line_ref
  - Consume amount
  
- [ ] **Balance validation** - before_submit:
  - Block submit if amount > balance

### 4.5 Permission Query Conditions (PQC)
- [ ] Create PQC on Project to filter by division based on User Permission
- [ ] Create PQC on Sales Invoice to filter by division
- [ ] Create PQC on Purchase Invoice to filter by division
- [ ] Create PQC on Purchase Order to filter by division
- [ ] Create PQC on Employee Advance to filter by division
- [ ] Create PQC on Expense Claim to filter by division
- [ ] Create PQC on Payment Entry to filter by division

## Phase 5: Client Scripts (Auto-fill)

### 5.1 Division Auto-fill
- [ ] Auto-fill division from Project on Sales Invoice
- [ ] Auto-fill division from Project on Purchase Invoice
- [ ] Auto-fill division from Project on Purchase Order
- [ ] Auto-fill division from Project on Employee Advance
- [ ] Auto-fill division from Project on Expense Claim
- [ ] Auto-fill division from Project on Payment Entry

### 5.2 Service Type Auto-fill
- [ ] Auto-set service_type from Item Group on Sales Invoice Item
- [ ] Auto-set service_type from Item Group on Purchase Invoice Item
- [ ] Auto-set service_type from Item Group on Expense Claim Detail
- [ ] Use SERVICE_TYPE_MAP from utils.constants

## Phase 6: Roles & Permissions

### 6.1 Custom Roles
- [ ] Create FF-OPS role
- [ ] Create FF-DOCS role
- [ ] Create FF-SALES role
- [ ] Create FF-FIN role
- [ ] Create FF-MANAGER role
- [ ] Create FF-ADMIN role
- [ ] Set permissions: Submit/cancel/amend finansial: FIN/MANAGER only

### 6.2 User Permissions
- [ ] Set up User Permission per user for Division access
- [ ] Configure Division-based access control

## Phase 7: Fixtures Export

### 7.1 Export Fixtures
- [ ] Export Custom Fields to JSON files in fixtures/ directory
- [ ] Export Property Setters to JSON files
- [ ] Export Custom DocTypes (FF Port, FF Airport, Advance Line, FF Consol Shipment) to JSON
- [ ] Export Tax Rule (1.1% JPT) to JSON
- [ ] Export Expense Claim Type defaults to JSON
- [ ] Update hooks.py fixtures list

## Phase 8: Data Import

### 8.1 Master Data Bootstrap
- [ ] Create CSV template for FF Port master data
- [ ] Create import script for FF Port (bootstrap common ports)
- [ ] Create CSV template for FF Airport master data
- [ ] Create import script for FF Airport (bootstrap common airports)

## Phase 9: Reports

### 9.1 Financial Reports
- [ ] **Project Service Breakdown**
  - Revenue: Sales Invoice Item.base_net_amount (si.project=filter, docstatus=1)
  - Cost: Purchase Invoice Item.base_net_amount + Expense Claim Detail.base_amount (project=filter, docstatus=1)
  - Group by: service category (Item Group primary; row.service_type fallback)
  - Output: revenue, cost, margin, margin%
  
- [ ] **Expense Claim Breakdown**
  - Sum by project × service_type × item
  
- [ ] **Advance Utilization**
  - Allocated/consumed/balance by project × advance × line
  
- [ ] **PO Commit vs Actual**
  - PO total vs (PI + EC) actual comparison
  
- [ ] **Project Financial Snapshot**
  - Counts (#SO, #SI, #PO, #PI, #EC, #PE)
  - Totals
  - AR/AP outstanding

### 9.2 Consol Reports (if enabled)
- [ ] **Consol Profitability**
  - Planned vs actual per consol & per member

## Phase 10: UI Enhancements

### 10.1 Project Dashboard Override
- [ ] Create dashboard override for Project
- [ ] Add sections: Sales (SI/SO), Purchases (PI/PO), Expenses (EC/EADV), Cash & Bank (PE)

### 10.2 Project Tab Finance
- [ ] Create Tab Finance with HTML embeds
- [ ] Add list for Employee Advances
- [ ] Add list for Expense Claims
- [ ] Add list for Purchase Orders
- [ ] Add list for Purchase Invoices
- [ ] Add list for Sales Invoices
- [ ] Add list for Payments
- [ ] Each list: Add/New button (preset project)
- [ ] Open-on-click functionality
- [ ] View All links

### 10.3 API Integration
- [ ] Whitelist list_by_project endpoint in hooks.py (already created in project/api.py)

## Phase 11: Rate Management (Optional but Recommended)

### 11.1 Rate Contract Doctypes
- [ ] **FF Rate Contract** (header)
  - Fields: vendor/carrier, mode, validity_from/to, currency, payment_term, status
  
- [ ] **FF Rate Lane** (child)
  - Sea: pol, pod, service(FCL/LCL), equipment, carrier, transit
  - Air: aoo, aod, airline, chargeable_rule, transit
  - Land: origin, destination, vehicle_type, basis(flat/per_km), distance
  
- [ ] **FF Rate Base** (child)
  - Base component per container/weight break
  
- [ ] **FF Rate Surcharge** (child)
  - code, calc_type(flat/per_kg/per_cntr/percent), taxable(Y/N)
  
- [ ] **FF Rate Freetime** (child Sea)
  - demurrage/detention/storage defaults
  
- [ ] **FF Pricing Rule**
  - markup/discount by division/mode/customer/commodity, priority, validity

### 11.2 Rate Engine
- [ ] Filter active + within validity by lane
- [ ] Calculate total buy = base + surcharges ± fuel index/FX
- [ ] Apply pricing rule → sell
- [ ] Return ranked options (cost, transit, carrier)

### 11.3 Rate Integration
- [ ] Integrate with Quotation: button "Find Rates" → inject items with sell plan
- [ ] Apply Tax Rule 1.1% on SI
- [ ] Integration with Project → PO (buy)
- [ ] Integration with Project → SI (sell + PPN 1.1%)
- [ ] Report: Planned vs Actual (Quotation planned vs PI + EC actual)

## Phase 12: CRM/Sales Integration

### 12.1 Opportunity/Quotation Enhancement
- [ ] Add required fields: division, mode, service_scope (Freight/Customs/Trucking/Port/Warehouse)
- [ ] Add lane fields: (POL/POD) or (AOO/AOD), ETD/ETA, incoterm
- [ ] Ensure items classified under "Freight Services" subtree

### 12.2 Auto Project Creation
- [ ] Create workflow: auto-create Project from Opp/Quotation Won
- [ ] Copy lane, division/mode/service_scope, incoterm, ETD/ETA
- [ ] Use dynamic naming series

## Phase 13: Consol Shipment (Optional)

### 13.1 Consol Processing
- [ ] Create allocation logic: Create one PI/EC at consol; split to PI/EC per project by allocation
- [ ] Create SI generation: Create SI per project member based on sell plan
- [ ] Principle: Keep financial documents 1:1 with Project for clean P&L and division access

## Phase 14: Data Backfill

### 14.1 Historical Data Migration
- [ ] Create script to set division on existing Projects, SI, PI, PO, EADV, EC, PE where missing
- [ ] Create script to link existing financial documents to Projects where missing

## Phase 15: Testing

### 15.1 Unit Tests
- [ ] Test naming series (Project & SI/PI/PO/EADV/EC)
- [ ] Test tax 1.1% auto-applied on SI for Freight Services items
- [ ] Test expense claim consumption (advance_line_ref & auto-pick)
- [ ] Test sum(Advance Line.allocated) == Employee Advance.advance_amount
- [ ] Test PQC filters list results by user division

### 15.2 Integration Tests
- [ ] E2E test: Lead→Quotation (Rate Finder)→Project→Task→PO→PI→EADV→EC→SI→PE→Reports

### 15.3 Coverage
- [ ] Achieve minimum 60% test coverage
- [ ] Target 80% test coverage

## Phase 16: Deployment & Release

### 16.1 Deployment Checklist
- [ ] Create deployment script: bench backup, migrate, build, restart, health checks
- [ ] Create rollback procedure: restore latest sql.gz + files
- [ ] Export fixtures: `bench --site <site> export-fixtures`

### 16.2 Release Gates (Must Pass)
- [ ] No core modification
- [ ] Dynamic naming active (Project & transactions)
- [ ] Division access (User Permission + PQC) enforced
- [ ] Project validations (mode→port/airport; ETD<ETA)
- [ ] Item Group tree + default accounts ready
- [ ] Sales Tax Rule 1.1% active; Purchase PPh23 via TWC
- [ ] Advance Line working; sum(allocated)=advance_amount
- [ ] EC rows have project+service_type; consumption validated
- [ ] PO/PI/SI valid; Reports OK
- [ ] Project UI (dashboard override + Tab Finance embeds)
- [ ] Tests green; coverage ≥ 60%; fixtures exported

## Migration Order Summary

1. ✅ Item Group tree → Default accounts
2. ✅ Tax templates & Tax Rule 1.1%
3. ✅ Custom Doctypes (FF Port/Airport, Advance Line, Consol*)
4. ✅ Custom Fields & Property Setters
5. ✅ Server Scripts (naming/validations/PQC)
6. ✅ Import FF Port/Airport CSV (bootstrap)
7. ✅ Reports
8. ✅ UI (dashboard override, Tab Finance)
9. ✅ Rate Management doctypes & engine
10. ✅ Data backfill (set division; link project where missing)

---

**Total Tasks: 71**
**Status: All pending - Ready to start Phase 1**

