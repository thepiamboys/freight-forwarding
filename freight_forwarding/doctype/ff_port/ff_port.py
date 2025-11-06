# -*- coding: utf-8 -*-
# Copyright (c) 2025, PT Kurhanz Trans and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FFPort(Document):
    """FF Port Master Document"""

    def validate(self):
        """Validate port data"""
        # Ensure port_code is uppercase
        if self.port_code:
            self.port_code = self.port_code.upper().strip()

        # Validate coordinates if provided
        if self.lat is not None:
            if not (-90 <= self.lat <= 90):
                frappe.throw("Latitude must be between -90 and 90")

        if self.lon is not None:
            if not (-180 <= self.lon <= 180):
                frappe.throw("Longitude must be between -180 and 180")

