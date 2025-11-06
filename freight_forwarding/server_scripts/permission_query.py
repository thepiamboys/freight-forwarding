# -*- coding: utf-8 -*-
"""
Permission Query Conditions (PQC) for Division-based Access Control
"""

import frappe


def get_division_filter(doctype, user=None):
    """
    Get division filter based on User Permission.
    Returns SQL condition string to filter by division.
    """
    if not user:
        user = frappe.session.user

    # Get user's allowed divisions from User Permission
    allowed_divisions = frappe.get_all(
        "User Permission",
        filters={
            "user": user,
            "allow": "Division",
            "for_value": ["!=", ""],
        },
        fields=["for_value"],
        distinct=True,
    )

    if not allowed_divisions:
        # If no User Permission set, return condition that matches nothing (admin can override)
        # For non-admin users, this will block access
        if "System Manager" in frappe.get_roles(user) or "FF-ADMIN" in frappe.get_roles(user):
            return None  # No filter for admin
        return "1=0"  # Block access

    division_list = [d.for_value for d in allowed_divisions]

    # Return SQL condition
    if len(division_list) == 1:
        return f"`tab{doctype}`.`division` = '{division_list[0]}'"
    else:
        divisions_str = "', '".join(division_list)
        return f"`tab{doctype}`.`division` IN ('{divisions_str}')"


def project_permission_query(user):
    """PQC for Project doctype"""
    condition = get_division_filter("Project", user)
    return condition


def sales_invoice_permission_query(user):
    """PQC for Sales Invoice doctype"""
    condition = get_division_filter("Sales Invoice", user)
    return condition


def purchase_invoice_permission_query(user):
    """PQC for Purchase Invoice doctype"""
    condition = get_division_filter("Purchase Invoice", user)
    return condition


def purchase_order_permission_query(user):
    """PQC for Purchase Order doctype"""
    condition = get_division_filter("Purchase Order", user)
    return condition


def employee_advance_permission_query(user):
    """PQC for Employee Advance doctype"""
    condition = get_division_filter("Employee Advance", user)
    return condition


def expense_claim_permission_query(user):
    """PQC for Expense Claim doctype"""
    condition = get_division_filter("Expense Claim", user)
    return condition


def payment_entry_permission_query(user):
    """PQC for Payment Entry doctype"""
    condition = get_division_filter("Payment Entry", user)
    return condition


def ff_consol_shipment_permission_query(user):
    """PQC for FF Consol Shipment doctype"""
    condition = get_division_filter("FF Consol Shipment", user)
    return condition

