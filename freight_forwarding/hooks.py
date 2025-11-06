# -*- coding: utf-8 -*-
"""
Hooks for Freight Forwarding App
"""

from . import __version__ as app_version

app_name = "freight_forwarding"
app_title = "Freight Forwarding"
app_publisher = "PT Kurhanz Trans"
app_description = "Enterprise-grade Freight Forwarding add-on for ERPNext v15"
app_icon = "octicon octicon-package"
app_color = "grey"
app_email = "dev@kurhanz.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_js = "/assets/freight_forwarding/js/freight_forwarding.js"
# app_include_css = "/assets/freight_forwarding/css/freight_forwarding.css"

# include js, css files in header of web template
# web_include_css = "/assets/freight_forwarding/css/freight_forwarding.css"
# web_include_js = "/assets/freight_forwarding/js/freight_forwarding.js"

# include custom scss in every website page (only file if you use web_include_css)
# website_theme_pages = ["freight_forwarding/pages"]

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Project": "freight_forwarding/project/client_scripts/project.js",
    "Sales Invoice": "freight_forwarding/project/client_scripts/sales_invoice.js",
    "Purchase Invoice": "freight_forwarding/project/client_scripts/purchase_invoice.js",
    "Purchase Order": "freight_forwarding/project/client_scripts/purchase_order.js",
    "Employee Advance": "freight_forwarding/project/client_scripts/employee_advance.js",
    "Expense Claim": "freight_forwarding/project/client_scripts/expense_claim.js",
    "Payment Entry": "freight_forwarding/project/client_scripts/payment_entry.js",
    "Quotation": "freight_forwarding/project/client_scripts/quotation.js",
    "FF Consol Shipment": "freight_forwarding/project/client_scripts/ff_consol_shipment.js",
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#   "Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#   "methods": "freight_forwarding.utils.jinja_methods",
#   "filters": "freight_forwarding.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "freight_forwarding.install.before_install"
# after_install = "freight_forwarding.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "freight_forwarding.uninstall.before_uninstall"
# after_uninstall = "freight_forwarding.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "freight_forwarding.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
    "Project": "freight_forwarding.server_scripts.permission_query.project_permission_query",
    "Sales Invoice": "freight_forwarding.server_scripts.permission_query.sales_invoice_permission_query",
    "Purchase Invoice": "freight_forwarding.server_scripts.permission_query.purchase_invoice_permission_query",
    "Purchase Order": "freight_forwarding.server_scripts.permission_query.purchase_order_permission_query",
    "Employee Advance": "freight_forwarding.server_scripts.permission_query.employee_advance_permission_query",
    "Expense Claim": "freight_forwarding.server_scripts.permission_query.expense_claim_permission_query",
    "Payment Entry": "freight_forwarding.server_scripts.permission_query.payment_entry_permission_query",
    "FF Consol Shipment": "freight_forwarding.server_scripts.permission_query.ff_consol_shipment_permission_query",
}

# has_permission = {
#   "Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#   "ToDo": "custom_app.overrides.custom_todo.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Project": {
        "before_insert": "freight_forwarding.server_scripts.naming_series.project_naming",
        "before_submit": "freight_forwarding.server_scripts.validations.project_validation",
    },
    "Sales Invoice": {
        "before_insert": "freight_forwarding.server_scripts.naming_series.sales_invoice_naming",
        "before_submit": "freight_forwarding.server_scripts.validations.sales_invoice_validation",
    },
    "Purchase Invoice": {
        "before_insert": "freight_forwarding.server_scripts.naming_series.purchase_invoice_naming",
        "before_submit": "freight_forwarding.server_scripts.validations.purchase_invoice_validation",
    },
    "Purchase Order": {
        "before_insert": "freight_forwarding.server_scripts.naming_series.purchase_order_naming",
        "before_submit": "freight_forwarding.server_scripts.validations.purchase_order_validation",
    },
    "Employee Advance": {
        "before_insert": "freight_forwarding.server_scripts.naming_series.employee_advance_naming",
        "before_save": "freight_forwarding.server_scripts.validations.employee_advance_validation",
    },
    "Expense Claim": {
        "before_insert": "freight_forwarding.server_scripts.naming_series.expense_claim_naming",
        "before_submit": [
            "freight_forwarding.server_scripts.validations.expense_claim_validation",
            "freight_forwarding.server_scripts.expense_claim_logic.expense_claim_consumption",
        ],
    },
    "Advance Line": {
        "validate": "freight_forwarding.server_scripts.expense_claim_logic.advance_line_balance_calculation",
    },
    "Opportunity": {
        "on_update": "freight_forwarding.server_scripts.crm_workflow.create_project_from_opportunity",
    },
    "Quotation": {
        "on_update": "freight_forwarding.server_scripts.crm_workflow.create_project_from_quotation",
        "validate": "freight_forwarding.server_scripts.crm_workflow.validate_quotation_items",
    },
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
#   "all": [
#     "freight_forwarding.tasks.all"
#   ],
#   "daily": [
#     "freight_forwarding.tasks.daily"
#   ],
#   "hourly": [
#     "freight_forwarding.tasks.hourly"
#   ],
#   "weekly": [
#     "freight_forwarding.tasks.weekly"
#   ],
#   "monthly": [
#     "freight_forwarding.tasks.monthly"
#   ]
# }

# Testing
# -------

# before_tests = "freight_forwarding.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
    "freight_forwarding.project.api.list_by_project": "freight_forwarding.project.api.list_by_project",
    "freight_forwarding.project.api.find_rates": "freight_forwarding.project.api.find_rates",
    "freight_forwarding.utils.import_data.import_ports_bootstrap": "freight_forwarding.utils.import_data.import_ports_bootstrap",
    "freight_forwarding.utils.import_data.import_airports_bootstrap": "freight_forwarding.utils.import_data.import_airports_bootstrap",
    "freight_forwarding.utils.consol.allocation.split_purchase_invoice": "freight_forwarding.utils.consol.allocation.split_purchase_invoice",
    "freight_forwarding.utils.consol.allocation.split_expense_claim": "freight_forwarding.utils.consol.allocation.split_expense_claim",
    "freight_forwarding.utils.consol.si_generation.create_si_per_member": "freight_forwarding.utils.consol.si_generation.create_si_per_member",
    "freight_forwarding.utils.backfill.data_backfill.backfill_division": "freight_forwarding.utils.backfill.data_backfill.backfill_division",
    "freight_forwarding.utils.backfill.data_backfill.backfill_project_links": "freight_forwarding.utils.backfill.data_backfill.backfill_project_links",
    "freight_forwarding.utils.backfill.data_backfill.backfill_expense_claim_project": "freight_forwarding.utils.backfill.data_backfill.backfill_expense_claim_project",
    "freight_forwarding.utils.backfill.data_backfill.run_all_backfills": "freight_forwarding.utils.backfill.data_backfill.run_all_backfills",
    "freight_forwarding.utils.verification.release_gates.run_all_gates": "freight_forwarding.utils.verification.release_gates.run_all_gates",
    "freight_forwarding.utils.verification.release_gates.verify_no_core_modification": "freight_forwarding.utils.verification.release_gates.verify_no_core_modification",
    "freight_forwarding.utils.verification.release_gates.verify_dynamic_naming": "freight_forwarding.utils.verification.release_gates.verify_dynamic_naming",
    "freight_forwarding.utils.verification.release_gates.verify_division_access": "freight_forwarding.utils.verification.release_gates.verify_division_access",
    "freight_forwarding.utils.verification.release_gates.verify_project_validations": "freight_forwarding.utils.verification.release_gates.verify_project_validations",
    "freight_forwarding.utils.verification.release_gates.verify_item_groups_and_accounts": "freight_forwarding.utils.verification.release_gates.verify_item_groups_and_accounts",
    "freight_forwarding.utils.verification.release_gates.verify_tax_configuration": "freight_forwarding.utils.verification.release_gates.verify_tax_configuration",
    "freight_forwarding.utils.verification.release_gates.verify_advance_line": "freight_forwarding.utils.verification.release_gates.verify_advance_line",
    "freight_forwarding.utils.verification.release_gates.verify_expense_claim": "freight_forwarding.utils.verification.release_gates.verify_expense_claim",
    "freight_forwarding.utils.verification.release_gates.verify_reports": "freight_forwarding.utils.verification.release_gates.verify_reports",
    "freight_forwarding.utils.verification.release_gates.verify_project_ui": "freight_forwarding.utils.verification.release_gates.verify_project_ui",
    "freight_forwarding.utils.verification.release_gates.verify_fixtures": "freight_forwarding.utils.verification.release_gates.verify_fixtures",
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
override_doctype_dashboards = {
    "Project": "freight_forwarding.project.dashboard.project_dashboard.get_dashboard_data"
}

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["freight_forwarding.utils.before_request"]
# after_request = ["freight_forwarding.utils.after_request"]

# Job Events
# ----------
# before_job = ["freight_forwarding.utils.before_job"]
# after_job = ["freight_forwarding.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#   {
#     "doctype": "{doctype_1}",
#     "filter_by": "{filter_by}",
#     "redact_fields": ["{field_1}", "{field_2}"],
#     "partial": 1,
#   },
#   {
#     "doctype": "{doctype_2}",
#     "filter_by": "{filter_by}",
#     "redact_fields": ["{field_1}", "{field_2}"],
#     "partial": 1,
#   },
#   {
#     "doctype": "{doctype_1}",
#     "filter_by": "{filter_by}",
#     "redact_fields": ["{field_1}", "{field_2}"],
#     "partial": 1,
#   },
# ]

# Authentication and authorization
# -----------------------------------

# auth_hooks = [
#   "freight_forwarding.auth.validate"
# ]

# Fixtures (will be loaded in order specified)
# ---------------------------------------------
fixtures = [
    # Roles
    "Role",
    # Expense Claim Types
    "Expense Claim Type",
    # Custom DocTypes
    "Custom DocType",
    # Custom Fields
    "Custom Field",
    # Property Setters
    "Property Setter",
    # Tax Rules
    "Tax Rule",
    # Note: Item Groups, Accounts, Tax Templates
    # should be imported manually via Data Import or bench import-doc
    # as they require company-specific configuration
]

