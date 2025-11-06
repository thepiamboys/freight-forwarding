# -*- coding: utf-8 -*-
# Copyright (c) 2025, PT Kurhanz Trans and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FFPricingRule(Document):
    """FF Pricing Rule DocType"""

    def validate(self):
        """Validate pricing rule"""
        self.validate_validity_dates()
        self.validate_markup_discount()

    def validate_validity_dates(self):
        """Validate validity_from < validity_to"""
        if self.validity_from and self.validity_to:
            if self.validity_from >= self.validity_to:
                frappe.throw("Validity From must be before Validity To.")

    def validate_markup_discount(self):
        """Validate that markup and discount are not both set"""
        if self.markup_value and self.discount_value:
            frappe.throw("Cannot set both Markup and Discount. Please set only one.")

