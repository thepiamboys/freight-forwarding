# -*- coding: utf-8 -*-
# Copyright (c) 2025, PT Kurhanz Trans and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FFRateContract(Document):
    """FF Rate Contract DocType"""

    def validate(self):
        """Validate rate contract"""
        self.validate_validity_dates()
        self.validate_mode_lanes()

    def validate_validity_dates(self):
        """Validate validity_from < validity_to"""
        if self.validity_from and self.validity_to:
            if self.validity_from >= self.validity_to:
                frappe.throw("Validity From must be before Validity To.")

    def validate_mode_lanes(self):
        """Validate that lanes match the mode"""
        if not self.rate_lanes:
            frappe.throw("At least one Rate Lane is required.")
        
        modes = (self.mode or "").split(",")
        modes = [m.strip() for m in modes]
        
        for lane in self.rate_lanes:
            if "Sea" in modes:
                if not lane.pol or not lane.pod:
                    frappe.throw(
                        f"Rate Lane {lane.idx}: POL and POD are required for Sea mode."
                    )
            
            if "Air" in modes:
                if not lane.aoo or not lane.aod:
                    frappe.throw(
                        f"Rate Lane {lane.idx}: AOO and AOD are required for Air mode."
                    )
            
            if "Land" in modes:
                if not lane.origin or not lane.destination:
                    frappe.throw(
                        f"Rate Lane {lane.idx}: Origin and Destination are required for Land mode."
                    )

