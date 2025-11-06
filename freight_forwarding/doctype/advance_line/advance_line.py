# -*- coding: utf-8 -*-
# Copyright (c) 2025, PT Kurhanz Trans and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AdvanceLine(Document):
    """Advance Line Child Document"""

    def validate(self):
        """Validate advance line data"""
        # Auto-fill item_group from item if not set
        if self.item and not self.item_group:
            item_group = frappe.db.get_value("Item", self.item, "item_group")
            if item_group:
                self.item_group = item_group

        # Calculate balance
        self.balance_amount = (self.allocated_amount or 0) - (self.consumed_amount or 0)

        # Update line status
        if self.balance_amount <= 0:
            self.line_status = "Closed"
        else:
            self.line_status = "Open"

