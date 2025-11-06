# -*- coding: utf-8 -*-
# Copyright (c) 2025, PT Kurhanz Trans and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    """
    PO Commit vs Actual Report
    
    Shows PO total vs (PI + EC) actual comparison
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
            "fieldname": "po_committed",
            "label": _("PO Committed"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "pi_actual",
            "label": _("PI Actual"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "ec_actual",
            "label": _("EC Actual"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "total_actual",
            "label": _("Total Actual"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "variance",
            "label": _("Variance"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "variance_percent",
            "label": _("Variance %"),
            "fieldtype": "Percent",
            "width": 100
        },
    ]


def get_data(filters):
    """Get report data"""
    conditions = []
    
    if filters.get("project"):
        conditions.append("po.project = %(project)s")
    
    if filters.get("from_date"):
        conditions.append("po.transaction_date >= %(from_date)s")
    
    if filters.get("to_date"):
        conditions.append("po.transaction_date <= %(to_date)s")
    
    where_clause = " AND " + " AND ".join(conditions) if conditions else ""
    
    # Get PO committed amounts
    po_data = frappe.db.sql(f"""
        SELECT 
            po.project,
            SUM(poi.base_amount) as po_committed
        FROM `tabPurchase Order` po
        INNER JOIN `tabPurchase Order Item` poi ON poi.parent = po.name
        WHERE po.docstatus = 1
            AND po.project IS NOT NULL
            {where_clause}
        GROUP BY po.project
    """, filters, as_dict=True)
    
    # Get PI actual
    pi_data = frappe.db.sql("""
        SELECT 
            pi.project,
            SUM(pii.base_amount) as pi_actual
        FROM `tabPurchase Invoice` pi
        INNER JOIN `tabPurchase Invoice Item` pii ON pii.parent = pi.name
        WHERE pi.docstatus = 1
            AND pi.project IS NOT NULL
        GROUP BY pi.project
    """, filters, as_dict=True)
    
    # Get EC actual
    ec_data = frappe.db.sql("""
        SELECT 
            ecd.project,
            SUM(ecd.amount) as ec_actual
        FROM `tabExpense Claim Detail` ecd
        INNER JOIN `tabExpense Claim` ec ON ecd.parent = ec.name
        WHERE ec.docstatus = 1
            AND ecd.project IS NOT NULL
        GROUP BY ecd.project
    """, filters, as_dict=True)
    
    # Combine data
    projects = set()
    po_dict = {row.project: row.po_committed for row in po_data}
    pi_dict = {row.project: row.pi_actual for row in pi_data}
    ec_dict = {row.project: row.ec_actual for row in ec_data}
    
    projects.update(po_dict.keys())
    projects.update(pi_dict.keys())
    projects.update(ec_dict.keys())
    
    result = []
    for project in sorted(projects):
        po_committed = po_dict.get(project, 0)
        pi_actual = pi_dict.get(project, 0)
        ec_actual = ec_dict.get(project, 0)
        total_actual = pi_actual + ec_actual
        variance = po_committed - total_actual
        variance_percent = (variance / po_committed * 100) if po_committed > 0 else 0
        
        result.append({
            "project": project,
            "po_committed": po_committed,
            "pi_actual": pi_actual,
            "ec_actual": ec_actual,
            "total_actual": total_actual,
            "variance": variance,
            "variance_percent": variance_percent,
        })
    
    return result

