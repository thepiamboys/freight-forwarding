# -*- coding: utf-8 -*-
"""
Consol Shipment Sales Invoice Generation

Create Sales Invoice per project member based on sell plan.
"""

import frappe
from frappe import _


def create_si_per_member(consol_shipment, sell_plan=None):
    """
    Create Sales Invoice per project member based on sell plan.
    
    Args:
        consol_shipment: FF Consol Shipment document
        sell_plan: dict of {project: [items]} or None to use default
    
    Returns:
        list: List of created Sales Invoice names
    """
    if not consol_shipment.consol_members:
        frappe.throw(_("No consol members found in consol shipment."))
    
    created_sis = []
    
    for member in consol_shipment.consol_members:
        if not member.project:
            continue
        
        # Get project details
        project = frappe.get_doc("Project", member.project)
        
        # Get customer from project or consol shipment
        customer = get_customer_for_project(project, consol_shipment)
        
        if not customer:
            frappe.msgprint(
                _(f"Customer not found for project {member.project}. Skipping SI creation."),
                alert=True
            )
            continue
        
        # Get items for this project
        if sell_plan and member.project in sell_plan:
            items = sell_plan[member.project]
        else:
            # Default: get items from project's quotation or opportunity
            items = get_default_items_for_project(project)
        
        if not items:
            frappe.msgprint(
                _(f"No items found for project {member.project}. Skipping SI creation."),
                alert=True
            )
            continue
        
        # Create Sales Invoice
        si_doc = frappe.get_doc({
            "doctype": "Sales Invoice",
            "customer": customer,
            "project": member.project,
            "posting_date": frappe.utils.today(),
            "due_date": frappe.utils.add_days(frappe.utils.today(), 30),
            "consol_shipment": consol_shipment.name,
            "company": project.company if hasattr(project, "company") else frappe.defaults.get_global_default("company"),
            "currency": frappe.defaults.get_global_default("currency"),
            "items": [],
        })
        
        # Add items
        for item_data in items:
            item_row = {
                "item_code": item_data.get("item_code"),
                "item_name": item_data.get("item_name"),
                "qty": item_data.get("qty", 1),
                "rate": item_data.get("rate", 0),
                "amount": item_data.get("amount", 0),
                "uom": item_data.get("uom"),
                "item_group": item_data.get("item_group"),
            }
            si_doc.append("items", item_row)
        
        # Set division from project
        if project.division:
            si_doc.division = project.division
        
        si_doc.insert()
        created_sis.append(si_doc.name)
    
    return created_sis


def get_customer_for_project(project, consol_shipment):
    """Get customer for project"""
    # Try to get from project's customer field if exists
    if hasattr(project, "customer") and project.customer:
        return project.customer
    
    # Try to get from linked Opportunity
    opportunity = frappe.db.get_value(
        "Opportunity",
        {"project": project.name},
        "party_name"
    )
    if opportunity:
        return opportunity
    
    # Try to get from linked Quotation
    quotation = frappe.db.get_value(
        "Quotation",
        {"project": project.name},
        "party_name"
    )
    if quotation:
        return quotation
    
    # Try to get from linked Sales Order
    sales_order = frappe.db.get_value(
        "Sales Order",
        {"project": project.name},
        "customer"
    )
    if sales_order:
        return sales_order
    
    return None


def get_default_items_for_project(project):
    """Get default items for project from linked Quotation or Opportunity"""
    items = []
    
    # Try to get from Quotation
    quotation = frappe.db.get_value(
        "Quotation",
        {"project": project.name, "docstatus": 1},
        "name"
    )
    
    if quotation:
        quotation_doc = frappe.get_doc("Quotation", quotation)
        for item in quotation_doc.items:
            items.append({
                "item_code": item.item_code,
                "item_name": item.item_name,
                "qty": item.qty,
                "rate": item.rate,
                "amount": item.amount,
                "uom": item.uom,
                "item_group": item.item_group,
            })
        return items
    
    # Try to get from Opportunity
    opportunity = frappe.db.get_value(
        "Opportunity",
        {"project": project.name},
        "name"
    )
    
    if opportunity:
        # Get items from linked Quotation if any
        linked_quotation = frappe.db.get_value(
            "Quotation",
            {"opportunity": opportunity},
            "name"
        )
        if linked_quotation:
            quotation_doc = frappe.get_doc("Quotation", linked_quotation)
            for item in quotation_doc.items:
                items.append({
                    "item_code": item.item_code,
                    "item_name": item.item_name,
                    "qty": item.qty,
                    "rate": item.rate,
                    "amount": item.amount,
                    "uom": item.uom,
                    "item_group": item.item_group,
                })
            return items
    
    return items

