# -*- coding: utf-8 -*-
"""
Server Scripts for Dynamic Naming Series
"""

import frappe
from frappe.model.naming import make_autoname
from freight_forwarding.utils.constants import DIVISION_CODES, MODE_CODES


def get_division_code(division):
    """Get division code from constants"""
    return DIVISION_CODES.get(division, "")


def get_mode_code(mode):
    """Get first mode code from mode string (MultiSelect)"""
    if not mode:
        return ""
    first_mode = mode.split("\n")[0].strip() if "\n" in mode else mode.split(",")[0].strip()
    return MODE_CODES.get(first_mode, "")


def project_naming(doc, method=None):
    """
    Generate dynamic naming for Project: {DIV}-{MODE}-{YYYYMMDD}-{###}
    Example: IMP-SEA-20251106-001
    """
    if doc.get("__islocal") != 1:
        return

    if not doc.division or not doc.mode:
        frappe.throw("Division & Mode wajib diisi untuk Project.")

    div_code = get_division_code(doc.division)
    mode_code = get_mode_code(doc.mode)

    if not div_code or not mode_code:
        frappe.throw("Division/Mode tidak valid.")

    today = frappe.utils.now_datetime().strftime("%Y%m%d")
    prefix = f"{div_code}-{mode_code}-{today}-"
    doc.name = make_autoname(prefix + "###")


def sales_invoice_naming(doc, method=None):
    """
    Generate dynamic naming for Sales Invoice: {DIV}-SINV-{YYYY}-{#####}
    Example: IMP-SINV-2025-00042
    """
    if doc.get("__islocal") != 1:
        return

    if not doc.project:
        frappe.throw("Sales Invoice wajib di-link ke Project.")

    division = frappe.db.get_value("Project", doc.project, "division")
    if not division:
        frappe.throw("Project tidak memiliki Division.")

    div_code = get_division_code(division)
    if not div_code:
        frappe.throw("Division tidak valid.")

    year = frappe.utils.now_datetime().strftime("%Y")
    prefix = f"{div_code}-SINV-{year}-"
    doc.name = make_autoname(prefix + "#####")


def purchase_invoice_naming(doc, method=None):
    """
    Generate dynamic naming for Purchase Invoice: {DIV}-PINV-{YYYY}-{#####}
    """
    if doc.get("__islocal") != 1:
        return

    if not doc.project:
        frappe.throw("Purchase Invoice wajib di-link ke Project.")

    division = frappe.db.get_value("Project", doc.project, "division")
    if not division:
        frappe.throw("Project tidak memiliki Division.")

    div_code = get_division_code(division)
    if not div_code:
        frappe.throw("Division tidak valid.")

    year = frappe.utils.now_datetime().strftime("%Y")
    prefix = f"{div_code}-PINV-{year}-"
    doc.name = make_autoname(prefix + "#####")


def purchase_order_naming(doc, method=None):
    """
    Generate dynamic naming for Purchase Order: {DIV}-PO-{YYYY}-{#####}
    """
    if doc.get("__islocal") != 1:
        return

    if not doc.project:
        frappe.throw("Purchase Order wajib di-link ke Project.")

    division = frappe.db.get_value("Project", doc.project, "division")
    if not division:
        frappe.throw("Project tidak memiliki Division.")

    div_code = get_division_code(division)
    if not div_code:
        frappe.throw("Division tidak valid.")

    year = frappe.utils.now_datetime().strftime("%Y")
    prefix = f"{div_code}-PO-{year}-"
    doc.name = make_autoname(prefix + "#####")


def employee_advance_naming(doc, method=None):
    """
    Generate dynamic naming for Employee Advance: {DIV}-EADV-{YYYY}-{#####}
    """
    if doc.get("__islocal") != 1:
        return

    if not doc.project:
        frappe.throw("Employee Advance wajib di-link ke Project.")

    division = frappe.db.get_value("Project", doc.project, "division")
    if not division:
        frappe.throw("Project tidak memiliki Division.")

    div_code = get_division_code(division)
    if not div_code:
        frappe.throw("Division tidak valid.")

    year = frappe.utils.now_datetime().strftime("%Y")
    prefix = f"{div_code}-EADV-{year}-"
    doc.name = make_autoname(prefix + "#####")


def expense_claim_naming(doc, method=None):
    """
    Generate dynamic naming for Expense Claim: {DIV}-EC-{YYYY}-{#####}
    """
    if doc.get("__islocal") != 1:
        return

    # Get division from first expense detail's project
    if not doc.expenses or len(doc.expenses) == 0:
        frappe.throw("Expense Claim harus memiliki minimal satu expense detail dengan Project.")

    first_expense = doc.expenses[0]
    if not first_expense.project:
        frappe.throw("Expense Claim detail wajib memiliki Project.")

    division = frappe.db.get_value("Project", first_expense.project, "division")
    if not division:
        frappe.throw("Project tidak memiliki Division.")

    div_code = get_division_code(division)
    if not div_code:
        frappe.throw("Division tidak valid.")

    year = frappe.utils.now_datetime().strftime("%Y")
    prefix = f"{div_code}-EC-{year}-"
    doc.name = make_autoname(prefix + "#####")

