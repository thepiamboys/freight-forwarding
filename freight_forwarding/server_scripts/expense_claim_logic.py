# -*- coding: utf-8 -*-
"""
Server Scripts for Expense Claim Consumption Logic
"""

import frappe
from frappe import _


def expense_claim_consumption(doc, method=None):
    """
    Handle Expense Claim consumption logic:
    - If advance_line_ref set → validate project & saldo, consume
    - Else if advance_ref set → auto-pick matching line → set advance_line_ref → consume
    - Block submit if amount > balance
    """
    if not doc.expenses:
        return

    for expense in doc.expenses:
        if not expense.project or not expense.amount:
            continue

        # Case 1: advance_line_ref is set
        if expense.advance_line_ref:
            validate_and_consume_advance_line(expense)

        # Case 2: advance_ref is set but advance_line_ref is not
        elif expense.advance_ref:
            auto_pick_and_consume(expense)


def validate_and_consume_advance_line(expense):
    """Validate and consume from specific advance line"""
    advance_line = frappe.get_doc("Advance Line", expense.advance_line_ref)

    # Validate project matches
    if advance_line.project != expense.project:
        frappe.throw(_("Advance Line project ({0}) tidak sesuai dengan Expense Claim detail project ({1}).").format(
            advance_line.project, expense.project
        ))

    # Validate balance
    balance = (advance_line.allocated_amount or 0) - (advance_line.consumed_amount or 0)
    if expense.amount > balance:
        frappe.throw(_("Amount ({0}) melebihi balance Advance Line ({1}).").format(
            expense.amount, balance
        ))

    # Consume amount
    advance_line.consumed_amount = (advance_line.consumed_amount or 0) + expense.amount
    advance_line.save()


def auto_pick_and_consume(expense):
    """Auto-pick matching advance line and consume"""
    if not expense.advance_ref or not expense.project:
        return

    # Find matching advance line
    # Match by: project, item (if set), service_type (if set)
    filters = {
        "parent": expense.advance_ref,
        "project": expense.project,
    }

    if expense.item:
        filters["item"] = expense.item

    if expense.service_type:
        filters["service_type"] = expense.service_type

    advance_lines = frappe.get_all(
        "Advance Line",
        filters=filters,
        fields=["name", "allocated_amount", "consumed_amount", "balance_amount"],
        order_by="creation asc"
    )

    # Find line with sufficient balance
    matching_line = None
    for line_data in advance_lines:
        balance = (line_data.allocated_amount or 0) - (line_data.consumed_amount or 0)
        if balance >= expense.amount:
            matching_line = line_data
            break

    if not matching_line:
        frappe.throw(_("Tidak ada Advance Line yang sesuai dengan saldo cukup untuk amount {0}.").format(
            expense.amount
        ))

    # Set advance_line_ref
    expense.advance_line_ref = matching_line.name

    # Consume amount
    advance_line = frappe.get_doc("Advance Line", matching_line.name)
    advance_line.consumed_amount = (advance_line.consumed_amount or 0) + expense.amount
    advance_line.save()


def advance_line_balance_calculation(doc, method=None):
    """
    Calculate Advance Line balance: balance = allocated - consumed
    Close when balance = 0
    """
    allocated = doc.allocated_amount or 0
    consumed = doc.consumed_amount or 0
    doc.balance_amount = allocated - consumed

    # Update line status
    if doc.balance_amount <= 0:
        doc.line_status = "Closed"
    else:
        doc.line_status = "Open"

