# -*- coding: utf-8 -*-
# Copyright (c) 2025, PT Kurhanz Trans and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    """
    Advance Utilization Report
    
    Shows allocated/consumed/balance by project × advance × line
    """
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    """Define report columns"""
    return [
        {
            "fieldname": "project",
            "label": _("Project"),
            "fieldtype": "Link",
            "options": "Project",
            "width": 150
        },
        {
            "fieldname": "advance",
            "label": _("Employee Advance"),
            "fieldtype": "Link",
            "options": "Employee Advance",
            "width": 150
        },
        {
            "fieldname": "advance_line",
            "label": _("Advance Line"),
            "fieldtype": "Link",
            "options": "Advance Line",
            "width": 150
        },
        {
            "fieldname": "item",
            "label": _("Item"),
            "fieldtype": "Link",
            "options": "Item",
            "width": 150
        },
        {
            "fieldname": "service_type",
            "label": _("Service Type"),
            "fieldtype": "Data",
            "width": 120
        },
        {
            "fieldname": "allocated_amount",
            "label": _("Allocated"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "consumed_amount",
            "label": _("Consumed"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "balance_amount",
            "label": _("Balance"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "line_status",
            "label": _("Status"),
            "fieldtype": "Data",
            "width": 80
        },
    ]


def get_data(filters):
    """Get report data"""
    conditions = []
    
    if filters.get("project"):
        conditions.append("al.project = %(project)s")
    
    if filters.get("advance"):
        conditions.append("al.parent = %(advance)s")
    
    if filters.get("service_type"):
        conditions.append("al.service_type = %(service_type)s")
    
    where_clause = " AND " + " AND ".join(conditions) if conditions else ""
    
    data = frappe.db.sql(f"""
        SELECT 
            al.project,
            al.parent as advance,
            al.name as advance_line,
            al.item,
            al.service_type,
            al.allocated_amount,
            al.consumed_amount,
            al.balance_amount,
            al.line_status
        FROM `tabAdvance Line` al
        INNER JOIN `tabEmployee Advance` ea ON al.parent = ea.name
        WHERE ea.docstatus != 2
            {where_clause}
        ORDER BY al.project, al.parent, al.name
    """, filters, as_dict=True)
    
    return data

