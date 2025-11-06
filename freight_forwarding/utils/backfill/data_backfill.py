# -*- coding: utf-8 -*-
"""
Data Backfill Scripts
For migrating existing data to FF structure
"""

import frappe
from frappe import _
from frappe.utils import now_datetime


@frappe.whitelist()
def backfill_division(dry_run=True):
    """
    Set division on existing documents where missing
    
    Args:
        dry_run: If True, only show what would be updated without making changes
    
    Returns:
        dict with summary of updates
    """
    results = {
        "updated": {},
        "skipped": {},
        "errors": []
    }
    
    doctypes = [
        "Project",
        "Sales Invoice",
        "Purchase Invoice",
        "Purchase Order",
        "Employee Advance",
        "Expense Claim",
        "Payment Entry"
    ]
    
    for doctype in doctypes:
        updated_count = 0
        skipped_count = 0
        
        try:
            # Get documents without division
            if doctype == "Project":
                # For Project, we need to set division based on some logic
                # For now, we'll skip Projects without division (user must set manually)
                docs = frappe.get_all(
                    doctype,
                    filters={"division": ["in", ["", None]]},
                    fields=["name"]
                )
            else:
                # For other doctypes, get those without division
                docs = frappe.get_all(
                    doctype,
                    filters={"division": ["in", ["", None]]},
                    fields=["name", "project"]
                )
            
            for doc in docs:
                if doctype == "Project":
                    # Skip Projects - must be set manually
                    skipped_count += 1
                    continue
                
                # Try to get division from linked Project
                if doc.get("project"):
                    division = frappe.db.get_value("Project", doc.project, "division")
                    if division:
                        if not dry_run:
                            frappe.db.set_value(doctype, doc.name, "division", division)
                            frappe.db.commit()
                        updated_count += 1
                    else:
                        skipped_count += 1
                else:
                    skipped_count += 1
        
        except Exception as e:
            results["errors"].append({
                "doctype": doctype,
                "error": str(e)
            })
        
        results["updated"][doctype] = updated_count
        results["skipped"][doctype] = skipped_count
    
    return results


@frappe.whitelist()
def backfill_project_links(dry_run=True):
    """
    Link existing financial documents to Projects where missing
    
    This is a helper script - actual linking should be done manually
    based on business logic (customer, supplier, dates, etc.)
    
    Args:
        dry_run: If True, only show what would be updated without making changes
    
    Returns:
        dict with summary
    """
    results = {
        "suggestions": {},
        "errors": []
    }
    
    doctypes = [
        "Sales Invoice",
        "Purchase Invoice",
        "Purchase Order",
        "Employee Advance",
        "Payment Entry"
    ]
    
    for doctype in doctypes:
        try:
            # Get documents without project
            if doctype == "Sales Invoice":
                docs = frappe.get_all(
                    doctype,
                    filters={"project": ["in", ["", None]], "docstatus": ["!=", 2]},
                    fields=["name", "customer", "posting_date", "grand_total"],
                    limit=100
                )
            elif doctype == "Purchase Invoice":
                docs = frappe.get_all(
                    doctype,
                    filters={"project": ["in", ["", None]], "docstatus": ["!=", 2]},
                    fields=["name", "supplier", "posting_date", "grand_total"],
                    limit=100
                )
            elif doctype == "Purchase Order":
                docs = frappe.get_all(
                    doctype,
                    filters={"project": ["in", ["", None]], "docstatus": ["!=", 2]},
                    fields=["name", "supplier", "transaction_date", "grand_total"],
                    limit=100
                )
            elif doctype == "Employee Advance":
                docs = frappe.get_all(
                    doctype,
                    filters={"project": ["in", ["", None]], "docstatus": ["!=", 2]},
                    fields=["name", "employee", "posting_date", "advance_amount"],
                    limit=100
                )
            elif doctype == "Payment Entry":
                docs = frappe.get_all(
                    doctype,
                    filters={"project": ["in", ["", None]], "docstatus": ["!=", 2]},
                    fields=["name", "party", "posting_date", "paid_amount"],
                    limit=100
                )
            
            results["suggestions"][doctype] = {
                "count": len(docs),
                "sample": docs[:5] if docs else []
            }
        
        except Exception as e:
            results["errors"].append({
                "doctype": doctype,
                "error": str(e)
            })
    
    return results


@frappe.whitelist()
def backfill_expense_claim_project(dry_run=True):
    """
    Set project on Expense Claim Detail rows where missing
    
    Args:
        dry_run: If True, only show what would be updated without making changes
    
    Returns:
        dict with summary
    """
    results = {
        "updated": 0,
        "skipped": 0,
        "errors": []
    }
    
    try:
        # Get Expense Claim Details without project
        ec_details = frappe.db.sql("""
            SELECT name, parent, expense_type, amount
            FROM `tabExpense Claim Detail`
            WHERE project IS NULL OR project = ''
            LIMIT 1000
        """, as_dict=True)
        
        for detail in ec_details:
            # Try to get project from parent Expense Claim
            # Note: This is a fallback - ideally project should be set on detail
            ec_project = frappe.db.get_value("Expense Claim", detail.parent, "project")
            
            if ec_project:
                if not dry_run:
                    frappe.db.set_value("Expense Claim Detail", detail.name, "project", ec_project)
                    frappe.db.commit()
                results["updated"] += 1
            else:
                results["skipped"] += 1
    
    except Exception as e:
        results["errors"].append(str(e))
    
    return results


@frappe.whitelist()
def run_all_backfills(dry_run=True):
    """
    Run all backfill scripts
    
    Args:
        dry_run: If True, only show what would be updated without making changes
    
    Returns:
        dict with all results
    """
    all_results = {
        "division": backfill_division(dry_run=dry_run),
        "project_links": backfill_project_links(dry_run=dry_run),
        "expense_claim_project": backfill_expense_claim_project(dry_run=dry_run),
        "dry_run": dry_run,
        "timestamp": now_datetime().isoformat()
    }
    
    return all_results

