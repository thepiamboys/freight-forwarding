# -*- coding: utf-8 -*-
# Copyright (c) 2025, PT Kurhanz Trans and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    """
    Project Financial Snapshot Report
    
    Shows counts, totals, AR/AP outstanding per project
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
            "fieldname": "so_count",
            "label": _("# SO"),
            "fieldtype": "Int",
            "width": 60
        },
        {
            "fieldname": "si_count",
            "label": _("# SI"),
            "fieldtype": "Int",
            "width": 60
        },
        {
            "fieldname": "po_count",
            "label": _("# PO"),
            "fieldtype": "Int",
            "width": 60
        },
        {
            "fieldname": "pi_count",
            "label": _("# PI"),
            "fieldtype": "Int",
            "width": 60
        },
        {
            "fieldname": "ec_count",
            "label": _("# EC"),
            "fieldtype": "Int",
            "width": 60
        },
        {
            "fieldname": "pe_count",
            "label": _("# PE"),
            "fieldtype": "Int",
            "width": 60
        },
        {
            "fieldname": "si_total",
            "label": _("SI Total"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "pi_total",
            "label": _("PI Total"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "ec_total",
            "label": _("EC Total"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "ar_outstanding",
            "label": _("AR Outstanding"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "ap_outstanding",
            "label": _("AP Outstanding"),
            "fieldtype": "Currency",
            "width": 120
        },
    ]


def get_data(filters):
    """Get report data"""
    conditions = []
    
    if filters.get("project"):
        conditions.append("p.name = %(project)s")
    
    if filters.get("division"):
        conditions.append("p.division = %(division)s")
    
    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
    
    data = frappe.db.sql(f"""
        SELECT 
            p.name as project,
            (SELECT COUNT(*) FROM `tabSales Order` WHERE project = p.name AND docstatus = 1) as so_count,
            (SELECT COUNT(*) FROM `tabSales Invoice` WHERE project = p.name AND docstatus = 1) as si_count,
            (SELECT COUNT(*) FROM `tabPurchase Order` WHERE project = p.name AND docstatus = 1) as po_count,
            (SELECT COUNT(*) FROM `tabPurchase Invoice` WHERE project = p.name AND docstatus = 1) as pi_count,
            (SELECT COUNT(DISTINCT ec.name) FROM `tabExpense Claim` ec
             INNER JOIN `tabExpense Claim Detail` ecd ON ecd.parent = ec.name
             WHERE ecd.project = p.name AND ec.docstatus = 1) as ec_count,
            (SELECT COUNT(*) FROM `tabPayment Entry` WHERE project = p.name AND docstatus = 1) as pe_count,
            (SELECT SUM(grand_total) FROM `tabSales Invoice` WHERE project = p.name AND docstatus = 1) as si_total,
            (SELECT SUM(grand_total) FROM `tabPurchase Invoice` WHERE project = p.name AND docstatus = 1) as pi_total,
            (SELECT SUM(ecd.amount) FROM `tabExpense Claim Detail` ecd
             INNER JOIN `tabExpense Claim` ec ON ecd.parent = ec.name
             WHERE ecd.project = p.name AND ec.docstatus = 1) as ec_total,
            (SELECT SUM(outstanding_amount) FROM `tabSales Invoice` WHERE project = p.name AND docstatus = 1 AND outstanding_amount > 0) as ar_outstanding,
            (SELECT SUM(outstanding_amount) FROM `tabPurchase Invoice` WHERE project = p.name AND docstatus = 1 AND outstanding_amount > 0) as ap_outstanding
        FROM `tabProject` p
        {where_clause}
        ORDER BY p.name
    """, filters, as_dict=True)
    
    return data

