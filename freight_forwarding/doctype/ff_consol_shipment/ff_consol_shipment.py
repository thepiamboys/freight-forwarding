# -*- coding: utf-8 -*-
# Copyright (c) 2025, PT Kurhanz Trans and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FFConsolShipment(Document):
    """FF Consol Shipment DocType"""

    def validate(self):
        """Validate consol shipment"""
        self.validate_mode_ports()
        self.validate_dates()
        self.validate_consol_members()
        self.validate_allocation_rules()

    def validate_mode_ports(self):
        """Validate that Sea mode requires POL/POD, Air mode requires AOO/AOD"""
        modes = (self.mode or "").split(",")
        modes = [m.strip() for m in modes]

        if "Sea" in modes:
            if not self.pol or not self.pod:
                frappe.throw(
                    "POL (Port of Loading) and POD (Port of Discharge) are required for Sea mode."
                )

        if "Air" in modes:
            if not self.aoo or not self.aod:
                frappe.throw(
                    "AOO (Airport of Origin) and AOD (Airport of Destination) are required for Air mode."
                )

    def validate_dates(self):
        """Validate ETD < ETA"""
        if self.etd and self.eta:
            if self.etd >= self.eta:
                frappe.throw("ETD (Estimated Time of Departure) must be before ETA (Estimated Time of Arrival).")

    def validate_consol_members(self):
        """Validate consol members"""
        if not self.consol_members or len(self.consol_members) == 0:
            frappe.throw("At least one Consol Member is required.")

        # Check for duplicate projects
        projects = [m.project for m in self.consol_members if m.project]
        if len(projects) != len(set(projects)):
            frappe.throw("Duplicate projects found in Consol Members. Each project should appear only once.")

        # Validate project divisions match consol division
        for member in self.consol_members:
            if member.project:
                project_division = frappe.db.get_value("Project", member.project, "division")
                if project_division != self.division:
                    frappe.throw(
                        f"Project {member.project} has division '{project_division}' which does not match consol division '{self.division}'."
                    )

    def validate_allocation_rules(self):
        """Validate allocation rules"""
        if not self.allocation_rules or len(self.allocation_rules) == 0:
            # Allocation rules are optional
            return

        # Validate allocation methods
        valid_methods = ["by_cbm", "by_weight", "by_chargeable", "equal", "by_slot", "manual_pct"]
        for rule in self.allocation_rules:
            if rule.method and rule.method not in valid_methods:
                frappe.throw(
                    f"Invalid allocation method '{rule.method}'. Valid methods are: {', '.join(valid_methods)}"
                )

            if rule.method == "manual_pct":
                if not rule.manual_percentage:
                    frappe.throw("Manual percentage is required when allocation method is 'manual_pct'.")

