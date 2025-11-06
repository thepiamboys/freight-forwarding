# -*- coding: utf-8 -*-
# Copyright (c) 2025, PT Kurhanz Trans and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    """
    Expense Claim Breakdown Report
    
    Shows sum by project × service_type × item
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
            "fieldname": "service_type",
            "label": _("Service Type"),
            "fieldtype": "Data",
            "width": 120
        },
        {
            "fieldname": "item",
            "label": _("Item"),
            "fieldtype": "Link",
            "options": "Item",
            "width": 150
        },
        {
            "fieldname": "total_amount",
            "label": _("Total Amount"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "count",
            "label": _("Count"),
            "fieldtype": "Int",
            "width": 80
        },
    ]


def get_data(filters):
    """Get report data"""
    conditions = []
    
    if filters.get("project"):
        conditions.append("ecd.project = %(project)s")
    
    if filters.get("service_type"):
        conditions.append("ecd.service_type = %(service_type)s")
    
    if filters.get("from_date"):
        conditions.append("ec.expense_date >= %(from_date)s")
    
    if filters.get("to_date"):
        conditions.append("ec.expense_date <= %(to_date)s")
    
    where_clause = " AND " + " AND ".join(conditions) if conditions else ""
    
    data = frappe.db.sql(f"""
        SELECT 
            ecd.project,
            ecd.service_type,
            ecd.expense_type as item,
            SUM(ecd.amount) as total_amount,
            COUNT(*) as count
        FROM `tabExpense Claim Detail` ecd
        INNER JOIN `tabExpense Claim` ec ON ecd.parent = ec.name
        WHERE ec.docstatus = 1
            AND ecd.project IS NOT NULL
            AND ecd.service_type IS NOT NULL
            {where_clause}
        GROUP BY ecd.project, ecd.service_type, ecd.expense_type
        ORDER BY ecd.project, ecd.service_type, total_amount DESC
    """, filters, as_dict=True)
    
    return data

