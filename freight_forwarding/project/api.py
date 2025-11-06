# -*- coding: utf-8 -*-
"""
Project API endpoints
"""

import frappe
from frappe import _


@frappe.whitelist()
def list_by_project(doctype, project, fields=None, limit=20):
    """
    List documents filtered by project.
    
    Args:
        doctype: Document type to query
        project: Project name
        fields: Comma-separated list of fields to return
        limit: Maximum number of records to return
    
    Returns:
        list: List of documents
    """
    if not doctype or not project:
        frappe.throw(_("Doctype and Project are required."))
    
    # Special handling for Expense Claim (project is in child table)
    if doctype == "Expense Claim":
        # First, find distinct Expense Claim names from Expense Claim Detail
        ec_names = frappe.db.sql("""
            SELECT DISTINCT parent
            FROM `tabExpense Claim Detail`
            WHERE project = %s
            AND parenttype = 'Expense Claim'
        """, (project,), as_dict=True)
        
        if not ec_names:
            return []
        
        names = [ec.parent for ec in ec_names]
        
        # Then fetch Expense Claim documents
        if fields:
            field_list = [f.strip() for f in fields.split(",")]
        else:
            field_list = ["*"]
        
        return frappe.get_all(
            "Expense Claim",
            filters={"name": ["in", names]},
            fields=field_list,
            limit=limit
        )
    
    # Standard handling for other doctypes
    if fields:
        field_list = [f.strip() for f in fields.split(",")]
    else:
        field_list = ["*"]
    
    filters = {"project": project}
    
    return frappe.get_all(
        doctype,
        filters=filters,
        fields=field_list,
        limit=limit
    )


@frappe.whitelist()
def find_rates(lane_type, origin, destination, mode, date_filter=None, weight=None, cbm=None, container_type=None):
    """
    Find rates for a given lane.
    
    Args:
        lane_type: "Sea", "Air", or "Land"
        origin: POL (for Sea), AOO (for Air), or origin city (for Land)
        destination: POD (for Sea), AOD (for Air), or destination city (for Land)
        mode: "Sea", "Air", or "Land"
        date_filter: Date to check validity (default: today)
        weight: Weight in kg (optional)
        cbm: Volume in CBM (optional)
        container_type: Container type for Sea (optional)
    
    Returns:
        list: Ranked rate options with buy/sell prices
    """
    from freight_forwarding.utils.rate.rate_engine import find_rates as engine_find_rates
    
    return engine_find_rates(
        lane_type=lane_type,
        origin=origin,
        destination=destination,
        mode=mode,
        date_filter=date_filter,
        weight=weight,
        cbm=cbm,
        container_type=container_type
    )
