# -*- coding: utf-8 -*-
"""
Project Dashboard Override
Customizes the Project dashboard with FF-specific sections
"""

import frappe
from frappe import _


def get_dashboard_data(data):
    """
    Override Project dashboard data
    
    Adds sections: Sales (SI/SO), Purchases (PI/PO), Expenses (EC/EADV), Cash & Bank (PE)
    """
    project = data.get("name")
    
    if not project:
        return data
    
    # Sales Section
    sales_invoices = frappe.get_list(
        "Sales Invoice",
        filters={"project": project, "docstatus": ["!=", 2]},
        fields=["name", "status", "posting_date", "grand_total", "outstanding_amount"],
        limit=5,
        order_by="posting_date desc"
    )
    
    sales_orders = frappe.get_list(
        "Sales Order",
        filters={"project": project, "docstatus": ["!=", 2]},
        fields=["name", "status", "transaction_date", "grand_total"],
        limit=5,
        order_by="transaction_date desc"
    )
    
    # Purchases Section
    purchase_invoices = frappe.get_list(
        "Purchase Invoice",
        filters={"project": project, "docstatus": ["!=", 2]},
        fields=["name", "status", "posting_date", "grand_total", "outstanding_amount"],
        limit=5,
        order_by="posting_date desc"
    )
    
    purchase_orders = frappe.get_list(
        "Purchase Order",
        filters={"project": project, "docstatus": ["!=", 2]},
        fields=["name", "status", "transaction_date", "grand_total"],
        limit=5,
        order_by="transaction_date desc"
    )
    
    # Expenses Section - get from Expense Claim Detail
    ec_names = frappe.db.sql("""
        SELECT DISTINCT parent
        FROM `tabExpense Claim Detail`
        WHERE project = %s
    """, (project,), as_dict=False)
    
    ec_list = [row[0] for row in ec_names] if ec_names else []
    
    expense_claims = []
    if ec_list:
        expense_claims = frappe.get_list(
            "Expense Claim",
            filters={"name": ["in", ec_list], "docstatus": ["!=", 2]},
            fields=["name", "status", "expense_date", "total_claimed_amount"],
            limit=5,
            order_by="expense_date desc"
        )
    
    employee_advances = frappe.get_list(
        "Employee Advance",
        filters={"project": project, "docstatus": ["!=", 2]},
        fields=["name", "status", "posting_date", "advance_amount"],
        limit=5,
        order_by="posting_date desc"
    )
    
    # Cash & Bank Section
    payment_entries = frappe.get_list(
        "Payment Entry",
        filters={"project": project, "docstatus": ["!=", 2]},
        fields=["name", "status", "posting_date", "paid_amount"],
        limit=5,
        order_by="posting_date desc"
    )
    
    # Add custom sections
    data["transactions"] = data.get("transactions", [])
    
    # Sales Section
    if sales_invoices or sales_orders:
        data["transactions"].append({
            "label": _("Sales"),
            "items": [
                {
                    "label": _("Sales Invoices"),
                    "count": len(sales_invoices),
                    "items": sales_invoices
                },
                {
                    "label": _("Sales Orders"),
                    "count": len(sales_orders),
                    "items": sales_orders
                }
            ]
        })
    
    # Purchases Section
    if purchase_invoices or purchase_orders:
        data["transactions"].append({
            "label": _("Purchases"),
            "items": [
                {
                    "label": _("Purchase Invoices"),
                    "count": len(purchase_invoices),
                    "items": purchase_invoices
                },
                {
                    "label": _("Purchase Orders"),
                    "count": len(purchase_orders),
                    "items": purchase_orders
                }
            ]
        })
    
    # Expenses Section
    if expense_claims or employee_advances:
        data["transactions"].append({
            "label": _("Expenses"),
            "items": [
                {
                    "label": _("Expense Claims"),
                    "count": len(expense_claims),
                    "items": expense_claims
                },
                {
                    "label": _("Employee Advances"),
                    "count": len(employee_advances),
                    "items": employee_advances
                }
            ]
        })
    
    # Cash & Bank Section
    if payment_entries:
        data["transactions"].append({
            "label": _("Cash & Bank"),
            "items": [
                {
                    "label": _("Payment Entries"),
                    "count": len(payment_entries),
                    "items": payment_entries
                }
            ]
        })
    
    return data

