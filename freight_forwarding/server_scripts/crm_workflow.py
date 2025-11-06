# -*- coding: utf-8 -*-
"""
CRM/Sales Workflow Scripts
Auto-create Project from Opportunity/Quotation Won
"""

import frappe
from frappe import _


def create_project_from_opportunity(doc, method=None):
    """
    Auto-create Project from Opportunity when status = "Won"
    """
    if doc.status != "Won":
        return
    
    # Check if project already exists
    if doc.project:
        return
    
    # Validate required fields
    if not doc.division:
        frappe.msgprint(_("Division is required to create Project from Opportunity."), alert=True)
        return
    
    if not doc.mode:
        frappe.msgprint(_("Mode is required to create Project from Opportunity."), alert=True)
        return
    
    # Create Project
    project = frappe.get_doc({
        "doctype": "Project",
        "project_name": doc.opportunity_name or doc.name,
        "customer": doc.party_name if doc.opportunity_from == "Customer" else None,
        "division": doc.division,
        "mode": doc.mode,
        "service_scope": doc.service_scope,
        "pol": doc.pol,
        "pod": doc.pod,
        "aoo": doc.aoo,
        "aod": doc.aod,
        "etd": doc.etd,
        "eta": doc.eta,
        "incoterm": doc.incoterm,
        "expected_start_date": doc.etd,
        "expected_end_date": doc.eta,
    })
    
    project.insert(ignore_permissions=True)
    
    # Link project to opportunity
    frappe.db.set_value("Opportunity", doc.name, "project", project.name)
    frappe.msgprint(_("Project {0} created from Opportunity.").format(project.name))


def create_project_from_quotation(doc, method=None):
    """
    Auto-create Project from Quotation when status = "Won"
    """
    if doc.status != "Won":
        return
    
    # Check if project already exists
    if doc.project:
        return
    
    # Validate required fields
    if not doc.division:
        frappe.msgprint(_("Division is required to create Project from Quotation."), alert=True)
        return
    
    if not doc.mode:
        frappe.msgprint(_("Mode is required to create Project from Quotation."), alert=True)
        return
    
    # Create Project
    project = frappe.get_doc({
        "doctype": "Project",
        "project_name": doc.title or doc.name,
        "customer": doc.party_name if doc.quotation_to == "Customer" else None,
        "division": doc.division,
        "mode": doc.mode,
        "service_scope": doc.service_scope,
        "pol": doc.pol,
        "pod": doc.pod,
        "aoo": doc.aoo,
        "aod": doc.aod,
        "etd": doc.etd,
        "eta": doc.eta,
        "incoterm": doc.incoterm,
        "expected_start_date": doc.etd,
        "expected_end_date": doc.eta,
    })
    
    project.insert(ignore_permissions=True)
    
    # Link project to quotation
    frappe.db.set_value("Quotation", doc.name, "project", project.name)
    frappe.msgprint(_("Project {0} created from Quotation.").format(project.name))


def validate_quotation_items(doc, method=None):
    """
    Ensure items in Quotation are classified under Freight Services subtree
    """
    if not doc.items:
        return
    
    freight_services_groups = frappe.db.sql("""
        SELECT name
        FROM `tabItem Group`
        WHERE parent_item_group = 'Freight Services'
           OR name = 'Freight Services'
    """, as_dict=True)
    
    valid_groups = [g.name for g in freight_services_groups]
    
    for item in doc.items:
        if item.item_code:
            item_group = frappe.db.get_value("Item", item.item_code, "item_group")
            if item_group and item_group not in valid_groups:
                frappe.throw(_(
                    "Item {0} (Item Group: {1}) must be under 'Freight Services' subtree. "
                    "Please classify the item correctly."
                ).format(item.item_code, item_group))

