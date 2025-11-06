// -*- coding: utf-8 -*-
/**
 * Client Script for FF Consol Shipment
 */

frappe.ui.form.on("FF Consol Shipment", {
    refresh: function(frm) {
        // Add button to split Purchase Invoice
        if (frm.doc.docstatus === 1 && !frm.is_new()) {
            frm.add_custom_button(__("Split Purchase Invoice"), function() {
                frappe.prompt({
                    fieldtype: "Link",
                    label: __("Purchase Invoice"),
                    fieldname: "purchase_invoice",
                    options: "Purchase Invoice",
                    reqd: 1,
                    filters: {
                        consol_shipment: frm.doc.name,
                        docstatus: 1
                    }
                }, function(data) {
                    frappe.call({
                        method: "freight_forwarding.utils.consol.allocation.split_purchase_invoice",
                        args: {
                            consol_shipment: frm.doc.name,
                            purchase_invoice_name: data.purchase_invoice
                        },
                        callback: function(r) {
                            if (r.message) {
                                frappe.msgprint({
                                    title: __("Success"),
                                    message: __("Purchase Invoice split successfully. Created {0} Purchase Invoices.", [r.message.length]),
                                    indicator: "green"
                                });
                                frm.reload_doc();
                            }
                        }
                    });
                });
            }, __("Actions"));

            // Add button to split Expense Claim
            frm.add_custom_button(__("Split Expense Claim"), function() {
                frappe.prompt({
                    fieldtype: "Link",
                    label: __("Expense Claim"),
                    fieldname: "expense_claim",
                    options: "Expense Claim",
                    reqd: 1,
                    filters: {
                        consol_shipment: frm.doc.name,
                        docstatus: 1
                    }
                }, function(data) {
                    frappe.call({
                        method: "freight_forwarding.utils.consol.allocation.split_expense_claim",
                        args: {
                            consol_shipment: frm.doc.name,
                            expense_claim_name: data.expense_claim
                        },
                        callback: function(r) {
                            if (r.message) {
                                frappe.msgprint({
                                    title: __("Success"),
                                    message: __("Expense Claim split successfully. Created {0} Expense Claims.", [r.message.length]),
                                    indicator: "green"
                                });
                                frm.reload_doc();
                            }
                        }
                    });
                });
            }, __("Actions"));

            // Add button to create Sales Invoices
            frm.add_custom_button(__("Create Sales Invoices"), function() {
                frappe.confirm(
                    __("This will create Sales Invoice for each consol member. Continue?"),
                    function() {
                        frappe.call({
                            method: "freight_forwarding.utils.consol.si_generation.create_si_per_member",
                            args: {
                                consol_shipment: frm.doc.name
                            },
                            callback: function(r) {
                                if (r.message) {
                                    frappe.msgprint({
                                        title: __("Success"),
                                        message: __("Created {0} Sales Invoices.", [r.message.length]),
                                        indicator: "green"
                                    });
                                    frm.reload_doc();
                                }
                            }
                        });
                    }
                );
            }, __("Actions"));
        }
    }
});

