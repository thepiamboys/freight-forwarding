# -*- coding: utf-8 -*-
"""
Consol Shipment Allocation Logic

Allocation methods:
- by_cbm: Allocate by CBM (Cubic Meter)
- by_weight: Allocate by Weight (kg)
- by_chargeable: Allocate by Chargeable Weight/Volume
- equal: Equal split among all members
- by_slot: Allocate by slot (1 slot per member)
- manual_pct: Manual percentage allocation
"""

import frappe
from frappe import _


def calculate_allocation(consol_shipment, total_amount, allocation_rule):
    """
    Calculate allocation amount for each consol member based on allocation rule.
    
    Args:
        consol_shipment: FF Consol Shipment document
        total_amount: Total amount to allocate
        allocation_rule: Allocation Rule document
    
    Returns:
        dict: {project: allocated_amount}
    """
    if not consol_shipment.consol_members:
        frappe.throw(_("No consol members found in consol shipment."))
    
    if not allocation_rule:
        # Default: equal allocation
        return equal_allocation(consol_shipment, total_amount)
    
    method = allocation_rule.method
    
    if method == "by_cbm":
        return by_cbm_allocation(consol_shipment, total_amount)
    elif method == "by_weight":
        return by_weight_allocation(consol_shipment, total_amount)
    elif method == "by_chargeable":
        return by_chargeable_allocation(consol_shipment, total_amount)
    elif method == "equal":
        return equal_allocation(consol_shipment, total_amount)
    elif method == "by_slot":
        return by_slot_allocation(consol_shipment, total_amount)
    elif method == "manual_pct":
        return manual_pct_allocation(consol_shipment, total_amount, allocation_rule)
    else:
        frappe.throw(_(f"Invalid allocation method: {method}"))


def by_cbm_allocation(consol_shipment, total_amount):
    """Allocate by CBM (Cubic Meter)"""
    total_cbm = sum([float(m.cbm or 0) for m in consol_shipment.consol_members])
    
    if total_cbm == 0:
        frappe.throw(_("Total CBM is zero. Cannot allocate by CBM."))
    
    allocation = {}
    for member in consol_shipment.consol_members:
        cbm = float(member.cbm or 0)
        percentage = cbm / total_cbm if total_cbm > 0 else 0
        allocation[member.project] = total_amount * percentage
    
    return allocation


def by_weight_allocation(consol_shipment, total_amount):
    """Allocate by Weight (kg)"""
    total_weight = sum([float(m.weight or 0) for m in consol_shipment.consol_members])
    
    if total_weight == 0:
        frappe.throw(_("Total weight is zero. Cannot allocate by weight."))
    
    allocation = {}
    for member in consol_shipment.consol_members:
        weight = float(member.weight or 0)
        percentage = weight / total_weight if total_weight > 0 else 0
        allocation[member.project] = total_amount * percentage
    
    return allocation


def by_chargeable_allocation(consol_shipment, total_amount):
    """Allocate by Chargeable Weight/Volume"""
    # Chargeable is the higher of weight or volume
    chargeable_values = []
    for member in consol_shipment.consol_members:
        weight = float(member.weight or 0)
        cbm = float(member.cbm or 0)
        # Convert CBM to weight equivalent (1 CBM = 1000 kg typically)
        cbm_weight = cbm * 1000
        chargeable = max(weight, cbm_weight)
        chargeable_values.append((member.project, chargeable))
    
    total_chargeable = sum([v[1] for v in chargeable_values])
    
    if total_chargeable == 0:
        frappe.throw(_("Total chargeable is zero. Cannot allocate by chargeable."))
    
    allocation = {}
    for project, chargeable in chargeable_values:
        percentage = chargeable / total_chargeable if total_chargeable > 0 else 0
        allocation[project] = total_amount * percentage
    
    return allocation


def equal_allocation(consol_shipment, total_amount):
    """Equal split among all members"""
    member_count = len(consol_shipment.consol_members)
    
    if member_count == 0:
        frappe.throw(_("No consol members found."))
    
    amount_per_member = total_amount / member_count
    
    allocation = {}
    for member in consol_shipment.consol_members:
        allocation[member.project] = amount_per_member
    
    return allocation


def by_slot_allocation(consol_shipment, total_amount):
    """Allocate by slot (1 slot per member)"""
    # Same as equal allocation
    return equal_allocation(consol_shipment, total_amount)


def manual_pct_allocation(consol_shipment, total_amount, allocation_rule):
    """Manual percentage allocation"""
    if not allocation_rule.manual_percentage:
        frappe.throw(_("Manual percentage is required for manual_pct allocation method."))
    
    # For manual_pct, we need to store percentage per member
    # This would require additional fields in Consol Member
    # For now, we'll use equal allocation as fallback
    frappe.msgprint(
        _("Manual percentage allocation requires percentage per member. Using equal allocation as fallback."),
        alert=True
    )
    return equal_allocation(consol_shipment, total_amount)


def split_purchase_invoice(consol_shipment, purchase_invoice_name):
    """
    Split a Purchase Invoice from consol shipment to individual PIs per project.
    
    Args:
        consol_shipment: FF Consol Shipment document
        purchase_invoice_name: Name of the consol Purchase Invoice
    
    Returns:
        list: List of created Purchase Invoice names
    """
    consol_pi = frappe.get_doc("Purchase Invoice", purchase_invoice_name)
    
    if not consol_pi:
        frappe.throw(_(f"Purchase Invoice {purchase_invoice_name} not found."))
    
    # Get allocation rules
    allocation_rules = consol_shipment.allocation_rules or []
    
    created_pis = []
    
    # For each item in consol PI, allocate to projects
    for item in consol_pi.items:
        # Find matching allocation rule
        allocation_rule = None
        for rule in allocation_rules:
            if rule.item == item.item_code or rule.charge_code == item.item_code:
                allocation_rule = rule
                break
        
        # Calculate allocation
        total_amount = item.base_amount
        allocation = calculate_allocation(consol_shipment, total_amount, allocation_rule)
        
        # Create PI per project
        for project, allocated_amount in allocation.items():
            # Check if PI for this project already exists
            existing_pi = frappe.db.exists(
                "Purchase Invoice",
                {
                    "project": project,
                    "consol_shipment": consol_shipment.name,
                    "docstatus": ["<", 2],
                }
            )
            
            if existing_pi:
                # Add item to existing PI
                pi_doc = frappe.get_doc("Purchase Invoice", existing_pi)
            else:
                # Create new PI
                pi_doc = frappe.get_doc({
                    "doctype": "Purchase Invoice",
                    "supplier": consol_pi.supplier,
                    "posting_date": consol_pi.posting_date,
                    "due_date": consol_pi.due_date,
                    "project": project,
                    "consol_shipment": consol_shipment.name,
                    "company": consol_pi.company,
                    "currency": consol_pi.currency,
                    "items": [],
                })
            
            # Add item with allocated amount
            item_row = {
                "item_code": item.item_code,
                "item_name": item.item_name,
                "qty": item.qty * (allocated_amount / total_amount) if total_amount > 0 else 0,
                "rate": item.rate,
                "amount": allocated_amount,
                "base_amount": allocated_amount,
                "uom": item.uom,
                "item_group": item.item_group,
            }
            
            pi_doc.append("items", item_row)
            
            if not existing_pi:
                pi_doc.insert()
                created_pis.append(pi_doc.name)
            else:
                pi_doc.save()
    
    # Cancel original consol PI
    if consol_pi.docstatus == 1:
        consol_pi.cancel()
    
    return created_pis


def split_expense_claim(consol_shipment, expense_claim_name):
    """
    Split an Expense Claim from consol shipment to individual ECs per project.
    
    Args:
        consol_shipment: FF Consol Shipment document
        expense_claim_name: Name of the consol Expense Claim
    
    Returns:
        list: List of created Expense Claim names
    """
    consol_ec = frappe.get_doc("Expense Claim", expense_claim_name)
    
    if not consol_ec:
        frappe.throw(_(f"Expense Claim {expense_claim_name} not found."))
    
    # Get allocation rules
    allocation_rules = consol_shipment.allocation_rules or []
    
    created_ecs = []
    
    # For each expense detail in consol EC, allocate to projects
    # Note: Expense Claim uses 'expenses' child table
    for expense_detail in consol_ec.expenses:
        # Find matching allocation rule
        allocation_rule = None
        for rule in allocation_rules:
            if rule.item == expense_detail.expense_type:
                allocation_rule = rule
                break
        
        # Calculate allocation
        total_amount = expense_detail.amount
        allocation = calculate_allocation(consol_shipment, total_amount, allocation_rule)
        
        # Create EC per project
        for project, allocated_amount in allocation.items():
            # Check if EC for this project already exists
            existing_ec = frappe.db.exists(
                "Expense Claim",
                {
                    "employee": consol_ec.employee,
                    "consol_shipment": consol_shipment.name,
                    "docstatus": ["<", 2],
                }
            )
            
            # Get project from Expense Claim Detail
            # Note: We need to check by project in Expense Claim Detail
            existing_ec_by_project = frappe.db.sql("""
                SELECT DISTINCT parent
                FROM `tabExpense Claim Detail`
                WHERE parenttype = 'Expense Claim'
                AND project = %s
                AND parent IN (
                    SELECT name FROM `tabExpense Claim`
                    WHERE consol_shipment = %s
                    AND docstatus < 2
                )
            """, (project, consol_shipment.name), as_dict=True)
            
            if existing_ec_by_project:
                # Add expense to existing EC
                ec_doc = frappe.get_doc("Expense Claim", existing_ec_by_project[0].parent)
            else:
                # Create new EC
                ec_doc = frappe.get_doc({
                    "doctype": "Expense Claim",
                    "employee": consol_ec.employee,
                    "expense_approver": consol_ec.expense_approver,
                    "posting_date": consol_ec.posting_date,
                    "consol_shipment": consol_shipment.name,
                    "company": consol_ec.company,
                    "currency": consol_ec.currency,
                    "expenses": [],
                })
            
            # Add expense detail with allocated amount
            expense_row = {
                "expense_date": expense_detail.expense_date,
                "expense_type": expense_detail.expense_type,
                "amount": allocated_amount,
                "description": expense_detail.description,
                "project": project,
            }
            
            ec_doc.append("expenses", expense_row)
            
            if not existing_ec_by_project:
                ec_doc.insert()
                created_ecs.append(ec_doc.name)
            else:
                ec_doc.save()
    
    # Cancel original consol EC
    if consol_ec.docstatus == 1:
        consol_ec.cancel()
    
    return created_ecs

