# -*- coding: utf-8 -*-
"""
Release Gates Verification Scripts
Automated verification for release gates
"""

import frappe
from frappe import _


@frappe.whitelist()
def verify_no_core_modification():
    """
    Gate 1: Verify no core modification
    """
    results = {
        "passed": True,
        "issues": []
    }
    
    # Check if any core files are modified
    # This is a basic check - full verification requires git diff
    try:
        # Check hooks.py doesn't override core classes
        import inspect
        from freight_forwarding import hooks
        
        # Check override_doctype_class
        if hasattr(hooks, 'override_doctype_class'):
            if hooks.override_doctype_class:
                results["issues"].append("override_doctype_class found - verify it's not modifying core")
        
        results["passed"] = len(results["issues"]) == 0
    except Exception as e:
        results["issues"].append(f"Error checking: {str(e)}")
        results["passed"] = False
    
    return results


@frappe.whitelist()
def verify_dynamic_naming():
    """
    Gate 2: Verify dynamic naming active
    """
    results = {
        "passed": True,
        "issues": []
    }
    
    # Check if naming functions exist
    try:
        from freight_forwarding.server_scripts import naming_series
        
        functions = [
            "project_naming",
            "sales_invoice_naming",
            "purchase_invoice_naming",
            "purchase_order_naming",
            "employee_advance_naming",
            "expense_claim_naming"
        ]
        
        for func_name in functions:
            if not hasattr(naming_series, func_name):
                results["issues"].append(f"Naming function {func_name} not found")
                results["passed"] = False
        
    except Exception as e:
        results["issues"].append(f"Error checking naming: {str(e)}")
        results["passed"] = False
    
    return results


@frappe.whitelist()
def verify_division_access():
    """
    Gate 3: Verify division access (PQC) enforced
    """
    results = {
        "passed": True,
        "issues": []
    }
    
    # Check if PQC functions exist
    try:
        from freight_forwarding.server_scripts import permission_query
        
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
            func_name = f"{doctype.lower().replace(' ', '_')}_permission_query"
            if not hasattr(permission_query, func_name):
                results["issues"].append(f"PQC function for {doctype} not found")
                results["passed"] = False
        
    except Exception as e:
        results["issues"].append(f"Error checking PQC: {str(e)}")
        results["passed"] = False
    
    return results


@frappe.whitelist()
def verify_project_validations():
    """
    Gate 4: Verify Project validations
    """
    results = {
        "passed": True,
        "issues": []
    }
    
    # Check if validation function exists
    try:
        from freight_forwarding.server_scripts import validations
        
        if not hasattr(validations, "project_validation"):
            results["issues"].append("Project validation function not found")
            results["passed"] = False
        
    except Exception as e:
        results["issues"].append(f"Error checking validations: {str(e)}")
        results["passed"] = False
    
    return results


@frappe.whitelist()
def verify_item_groups_and_accounts():
    """
    Gate 5: Verify Item Group tree + default accounts
    """
    results = {
        "passed": True,
        "issues": []
    }
    
    try:
        # Check Freight Services Item Group
        if not frappe.db.exists("Item Group", "Freight Services"):
            results["issues"].append("Item Group 'Freight Services' not found")
            results["passed"] = False
        
        # Check child groups
        child_groups = ["Freight", "Customs", "Trucking", "Port", "Warehouse", "Surcharges"]
        for group in child_groups:
            if not frappe.db.exists("Item Group", group):
                results["issues"].append(f"Item Group '{group}' not found")
                results["passed"] = False
        
    except Exception as e:
        results["issues"].append(f"Error checking item groups: {str(e)}")
        results["passed"] = False
    
    return results


@frappe.whitelist()
def verify_tax_configuration():
    """
    Gate 6: Verify Sales Tax Rule 1.1% and Purchase PPh23
    """
    results = {
        "passed": True,
        "issues": []
    }
    
    try:
        # Check Tax Rule
        if not frappe.db.exists("Tax Rule", "PPN JPT 1,1% - Freight Services"):
            results["issues"].append("Tax Rule 'PPN JPT 1,1% - Freight Services' not found")
            results["passed"] = False
        
        # Check Tax Withholding Category
        if not frappe.db.exists("Tax Withholding Category", "PPh 23"):
            results["issues"].append("Tax Withholding Category 'PPh 23' not found")
            results["passed"] = False
        
    except Exception as e:
        results["issues"].append(f"Error checking tax configuration: {str(e)}")
        results["passed"] = False
    
    return results


@frappe.whitelist()
def verify_advance_line():
    """
    Gate 7: Verify Advance Line working
    """
    results = {
        "passed": True,
        "issues": []
    }
    
    try:
        # Check if Advance Line doctype exists
        if not frappe.db.exists("DocType", "Advance Line"):
            results["issues"].append("DocType 'Advance Line' not found")
            results["passed"] = False
        
        # Check if validation function exists
        from freight_forwarding.server_scripts import validations
        if not hasattr(validations, "employee_advance_validation"):
            results["issues"].append("Employee Advance validation function not found")
            results["passed"] = False
        
    except Exception as e:
        results["issues"].append(f"Error checking advance line: {str(e)}")
        results["passed"] = False
    
    return results


@frappe.whitelist()
def verify_expense_claim():
    """
    Gate 8: Verify EC rows have project+service_type; consumption validated
    """
    results = {
        "passed": True,
        "issues": []
    }
    
    try:
        # Check if validation function exists
        from freight_forwarding.server_scripts import validations
        if not hasattr(validations, "expense_claim_validation"):
            results["issues"].append("Expense Claim validation function not found")
            results["passed"] = False
        
        # Check if consumption function exists
        from freight_forwarding.server_scripts import expense_claim_logic
        if not hasattr(expense_claim_logic, "expense_claim_consumption"):
            results["issues"].append("Expense Claim consumption function not found")
            results["passed"] = False
        
    except Exception as e:
        results["issues"].append(f"Error checking expense claim: {str(e)}")
        results["passed"] = False
    
    return results


@frappe.whitelist()
def verify_reports():
    """
    Gate 9: Verify Reports OK
    """
    results = {
        "passed": True,
        "issues": []
    }
    
    try:
        reports = [
            "Project Service Breakdown",
            "Expense Claim Breakdown",
            "Advance Utilization",
            "PO Commit vs Actual",
            "Project Financial Snapshot"
        ]
        
        for report_name in reports:
            if not frappe.db.exists("Report", report_name):
                results["issues"].append(f"Report '{report_name}' not found")
                results["passed"] = False
        
    except Exception as e:
        results["issues"].append(f"Error checking reports: {str(e)}")
        results["passed"] = False
    
    return results


@frappe.whitelist()
def verify_project_ui():
    """
    Gate 10: Verify Project UI
    """
    results = {
        "passed": True,
        "issues": []
    }
    
    try:
        # Check if dashboard override exists
        from freight_forwarding.project.dashboard import project_dashboard
        if not hasattr(project_dashboard, "get_dashboard_data"):
            results["issues"].append("Project dashboard override not found")
            results["passed"] = False
        
        # Check if client script exists
        import os
        client_script_path = "freight_forwarding/project/client_scripts/project.js"
        if not os.path.exists(client_script_path):
            results["issues"].append("Project client script not found")
            results["passed"] = False
        
    except Exception as e:
        results["issues"].append(f"Error checking project UI: {str(e)}")
        results["passed"] = False
    
    return results


@frappe.whitelist()
def verify_fixtures():
    """
    Gate 11: Verify fixtures exported
    """
    results = {
        "passed": True,
        "issues": []
    }
    
    try:
        import os
        
        fixtures_dir = "freight_forwarding/fixtures"
        required_fixtures = [
            "custom_field.json",
            "property_setter.json",
            "custom_doctype.json",
            "tax_rule.json",
            "expense_claim_type.json",
            "role.json"
        ]
        
        for fixture in required_fixtures:
            fixture_path = os.path.join(fixtures_dir, fixture)
            if not os.path.exists(fixture_path):
                results["issues"].append(f"Fixture '{fixture}' not found")
                results["passed"] = False
        
    except Exception as e:
        results["issues"].append(f"Error checking fixtures: {str(e)}")
        results["passed"] = False
    
    return results


@frappe.whitelist()
def run_all_gates():
    """
    Run all release gates verification
    """
    gates = {
        "gate_1_no_core_modification": verify_no_core_modification(),
        "gate_2_dynamic_naming": verify_dynamic_naming(),
        "gate_3_division_access": verify_division_access(),
        "gate_4_project_validations": verify_project_validations(),
        "gate_5_item_groups_accounts": verify_item_groups_and_accounts(),
        "gate_6_tax_configuration": verify_tax_configuration(),
        "gate_7_advance_line": verify_advance_line(),
        "gate_8_expense_claim": verify_expense_claim(),
        "gate_9_reports": verify_reports(),
        "gate_10_project_ui": verify_project_ui(),
        "gate_11_fixtures": verify_fixtures(),
    }
    
    all_passed = all(gate["passed"] for gate in gates.values())
    
    return {
        "all_passed": all_passed,
        "gates": gates,
        "summary": {
            "total": len(gates),
            "passed": sum(1 for gate in gates.values() if gate["passed"]),
            "failed": sum(1 for gate in gates.values() if not gate["passed"])
        }
    }

