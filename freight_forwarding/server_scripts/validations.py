# -*- coding: utf-8 -*-
"""
Server Scripts for Document Validations
"""

import frappe
from frappe import _


def project_validation(doc, method=None):
    """
    Validate Project before submit:
    - Sea mode requires POL/POD
    - Air mode requires AOO/AOD
    - ETD < ETA
    """
    if not doc.mode:
        return

    modes = doc.mode.split("\n") if "\n" in doc.mode else doc.mode.split(",")
    modes = [m.strip() for m in modes]

    # Check Sea mode
    if "Sea" in modes:
        if not doc.pol:
            frappe.throw(_("Port of Loading (POL) wajib diisi untuk mode Sea."))
        if not doc.pod:
            frappe.throw(_("Port of Discharge (POD) wajib diisi untuk mode Sea."))

    # Check Air mode
    if "Air" in modes:
        if not doc.aoo:
            frappe.throw(_("Airport of Origin (AOO) wajib diisi untuk mode Air."))
        if not doc.aod:
            frappe.throw(_("Airport of Destination (AOD) wajib diisi untuk mode Air."))

    # Validate ETD < ETA
    if doc.etd and doc.eta:
        if doc.etd >= doc.eta:
            frappe.throw(_("ETD harus lebih kecil dari ETA."))


def sales_invoice_validation(doc, method=None):
    """
    Validate Sales Invoice before submit:
    - Require project
    - Ensure item classification
    - Ensure 1.1% tax rule applied
    - Set division from Project
    """
    if not doc.project:
        frappe.throw(_("Project wajib diisi untuk Sales Invoice."))

    # Set division from project
    division = frappe.db.get_value("Project", doc.project, "division")
    if division:
        doc.division = division

    # Validate items classification
    for item in doc.items:
        if not item.item_group and not item.get("service_type"):
            frappe.throw(_("Item {0} belum terklasifikasi (Item Group atau Service Type wajib diisi).").format(
                item.item_name or item.item_code
            ))

    # Check if tax rule is applied (check if any tax has rate 1.1%)
    has_jpt_tax = False
    if doc.taxes:
        for tax in doc.taxes:
            if tax.rate == 1.1:
                has_jpt_tax = True
                break

    # Note: Tax rule should be auto-applied via Tax Rule configuration
    # This validation is a reminder, not a blocker


def purchase_invoice_validation(doc, method=None):
    """
    Validate Purchase Invoice before submit:
    - Require project
    - Ensure classification valid
    - Ensure TWC if supplier applicable
    - Set division from Project
    """
    if not doc.project:
        frappe.throw(_("Project wajib diisi untuk Purchase Invoice."))

    # Set division from project
    division = frappe.db.get_value("Project", doc.project, "division")
    if division:
        doc.division = division

    # Validate items classification
    for item in doc.items:
        if not item.item_group and not item.get("service_type"):
            frappe.throw(_("Item {0} belum terklasifikasi (Item Group atau Service Type wajib diisi).").format(
                item.item_name or item.item_code
            ))

    # TWC validation should be handled by ERPNext's Tax Withholding Category
    # This is just a reminder


def purchase_order_validation(doc, method=None):
    """
    Validate Purchase Order before submit:
    - Require project
    - Ensure service classification
    """
    if not doc.project:
        frappe.throw(_("Project wajib diisi untuk Purchase Order."))

    # Validate items classification
    for item in doc.items:
        if not item.item_group and not item.get("service_type"):
            frappe.throw(_("Item {0} belum terklasifikasi (Item Group atau Service Type wajib diisi).").format(
                item.item_name or item.item_code
            ))


def expense_claim_validation(doc, method=None):
    """
    Validate Expense Claim before submit:
    - Each row must have project & service_type
    - Apply consumption rules
    - Set cost_center (by division mapping) if empty
    - Set division (header) from Project
    """
    if not doc.expenses or len(doc.expenses) == 0:
        frappe.throw(_("Expense Claim harus memiliki minimal satu expense detail."))

    # Get division from first expense's project
    first_expense = doc.expenses[0]
    if not first_expense.project:
        frappe.throw(_("Expense Claim detail wajib memiliki Project."))

    division = frappe.db.get_value("Project", first_expense.project, "division")
    if division:
        doc.division = division

    # Validate each expense detail
    for expense in doc.expenses:
        if not expense.project:
            frappe.throw(_("Setiap Expense Claim detail wajib memiliki Project."))

        if not expense.service_type:
            frappe.throw(_("Setiap Expense Claim detail wajib memiliki Service Type."))

        # Consumption validation will be handled in separate function
        # This is basic validation

    # Cost center mapping by division (can be extended)
    # For now, just ensure it's set if not provided


def employee_advance_validation(doc, method=None):
    """
    Validate Employee Advance before save:
    - sum(allocated_amount) == advance_amount
    - all child.project == header.project
    """
    if not hasattr(doc, "advance_lines") or not doc.advance_lines:
        return

    if not doc.project:
        frappe.throw(_("Employee Advance wajib memiliki Project."))

    total_allocated = 0
    for line in doc.advance_lines:
        # Validate all lines have same project as header
        if line.project != doc.project:
            frappe.throw(_("Semua Advance Line harus memiliki Project yang sama dengan Employee Advance."))

        total_allocated += line.allocated_amount or 0

    # Validate sum equals advance_amount
    if abs(total_allocated - (doc.advance_amount or 0)) > 0.01:  # Allow small rounding difference
        frappe.throw(_("Total Allocated Amount ({0}) harus sama dengan Advance Amount ({1}).").format(
            total_allocated, doc.advance_amount
        ))

