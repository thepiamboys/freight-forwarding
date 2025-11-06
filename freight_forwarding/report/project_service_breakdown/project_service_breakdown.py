# -*- coding: utf-8 -*-
# Copyright (c) 2025, PT Kurhanz Trans and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    """
    Project Service Breakdown Report
    
    Shows revenue, cost, margin, and margin% grouped by service category
    """
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    """Define report columns"""
    return [
        {
            "fieldname": "service_category",
            "label": _("Service Category"),
            "fieldtype": "Data",
            "width": 150
        },
        {
            "fieldname": "revenue",
            "label": _("Revenue"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "cost",
            "label": _("Cost"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "margin",
            "label": _("Margin"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "margin_percent",
            "label": _("Margin %"),
            "fieldtype": "Percent",
            "width": 100
        },
    ]


def get_data(filters):
    """Get report data"""
    project = filters.get("project")
    if not project:
        frappe.throw(_("Project is required"))

    # Get revenue from Sales Invoice Items
    revenue_data = get_revenue_data(project, filters)
    
    # Get cost from Purchase Invoice Items + Expense Claim Details
    cost_data = get_cost_data(project, filters)
    
    # Combine and calculate margins
    service_categories = set()
    service_categories.update(revenue_data.keys())
    service_categories.update(cost_data.keys())
    
    result = []
    total_revenue = 0
    total_cost = 0
    
    for category in sorted(service_categories):
        revenue = revenue_data.get(category, 0)
        cost = cost_data.get(category, 0)
        margin = revenue - cost
        margin_percent = (margin / revenue * 100) if revenue > 0 else 0
        
        total_revenue += revenue
        total_cost += cost
        
        result.append({
            "service_category": category,
            "revenue": revenue,
            "cost": cost,
            "margin": margin,
            "margin_percent": margin_percent,
        })
    
    # Add total row
    total_margin = total_revenue - total_cost
    total_margin_percent = (total_margin / total_revenue * 100) if total_revenue > 0 else 0
    
    result.append({
        "service_category": "<b>TOTAL</b>",
        "revenue": total_revenue,
        "cost": total_cost,
        "margin": total_margin,
        "margin_percent": total_margin_percent,
    })
    
    return result


def get_revenue_data(project, filters):
    """Get revenue grouped by service category"""
    revenue_by_category = {}
    
    # Get from Sales Invoice Items
    si_items = frappe.db.sql("""
        SELECT 
            COALESCE(sii.service_type, ig.name) as service_category,
            SUM(sii.base_net_amount) as revenue
        FROM `tabSales Invoice Item` sii
        INNER JOIN `tabSales Invoice` si ON sii.parent = si.name
        LEFT JOIN `tabItem` i ON sii.item_code = i.name
        LEFT JOIN `tabItem Group` ig ON i.item_group = ig.name
        WHERE si.project = %s
            AND si.docstatus = 1
            AND (ig.parent_item_group = 'Freight Services' OR ig.name = 'Freight Services')
        GROUP BY service_category
    """, (project,), as_dict=True)
    
    for row in si_items:
        category = row.service_category or "Unclassified"
        revenue_by_category[category] = row.revenue or 0
    
    return revenue_by_category


def get_cost_data(project, filters):
    """Get cost grouped by service category"""
    cost_by_category = {}
    
    # Get from Purchase Invoice Items
    pi_items = frappe.db.sql("""
        SELECT 
            COALESCE(pii.service_type, ig.name) as service_category,
            SUM(pii.base_net_amount) as cost
        FROM `tabPurchase Invoice Item` pii
        INNER JOIN `tabPurchase Invoice` pi ON pii.parent = pi.name
        LEFT JOIN `tabItem` i ON pii.item_code = i.name
        LEFT JOIN `tabItem Group` ig ON i.item_group = ig.name
        WHERE pi.project = %s
            AND pi.docstatus = 1
            AND (ig.parent_item_group = 'Freight Services' OR ig.name = 'Freight Services')
        GROUP BY service_category
    """, (project,), as_dict=True)
    
    for row in pi_items:
        category = row.service_category or "Unclassified"
        cost_by_category[category] = cost_by_category.get(category, 0) + (row.cost or 0)
    
    # Get from Expense Claim Details
    ec_items = frappe.db.sql("""
        SELECT 
            ecd.service_type as service_category,
            SUM(ecd.amount) as cost
        FROM `tabExpense Claim Detail` ecd
        INNER JOIN `tabExpense Claim` ec ON ecd.parent = ec.name
        WHERE ecd.project = %s
            AND ec.docstatus = 1
            AND ecd.service_type IS NOT NULL
        GROUP BY ecd.service_type
    """, (project,), as_dict=True)
    
    for row in ec_items:
        category = row.service_category or "Unclassified"
        cost_by_category[category] = cost_by_category.get(category, 0) + (row.cost or 0)
    
    return cost_by_category

