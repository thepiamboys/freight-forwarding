// Quotation Client Script
// Validates items are under Freight Services subtree

frappe.ui.form.on('Quotation', {
    refresh: function(frm) {
        // Add custom button for Find Rates
        if (frm.doc.docstatus === 0 && frm.doc.mode && (frm.doc.pol || frm.doc.aoo)) {
            frm.add_custom_button(__('Find Rates'), function() {
                find_rates_for_quotation(frm);
            }, __('Tools'));
        }
    },
    
    validate: function(frm) {
        // Validate items are under Freight Services
        if (frm.doc.items && frm.doc.items.length > 0) {
            frm.doc.items.forEach(function(item) {
                if (item.item_code) {
                    frappe.db.get_value('Item', item.item_code, 'item_group', function(r) {
                        if (r && r.item_group) {
                            frappe.db.get_value('Item Group', r.item_group, 'parent_item_group', function(ig) {
                                if (ig && ig.parent_item_group !== 'Freight Services' && r.item_group !== 'Freight Services') {
                                    frappe.msgprint(__('Item {0} must be under Freight Services subtree.', [item.item_code]));
                                }
                            });
                        }
                    });
                }
            });
        }
    }
});

// Auto-fill division, mode, service_scope from Opportunity if linked
frappe.ui.form.on('Quotation', {
    opportunity: function(frm) {
        if (frm.doc.opportunity) {
            frappe.db.get_value('Opportunity', frm.doc.opportunity, [
                'division', 'mode', 'service_scope', 'pol', 'pod', 'aoo', 'aod', 'etd', 'eta', 'incoterm'
            ], function(r) {
                if (r.message) {
                    if (r.message.division && !frm.doc.division) {
                        frm.set_value('division', r.message.division);
                    }
                    if (r.message.mode && !frm.doc.mode) {
                        frm.set_value('mode', r.message.mode);
                    }
                    if (r.message.service_scope && !frm.doc.service_scope) {
                        frm.set_value('service_scope', r.message.service_scope);
                    }
                    if (r.message.pol && !frm.doc.pol) {
                        frm.set_value('pol', r.message.pol);
                    }
                    if (r.message.pod && !frm.doc.pod) {
                        frm.set_value('pod', r.message.pod);
                    }
                    if (r.message.aoo && !frm.doc.aoo) {
                        frm.set_value('aoo', r.message.aoo);
                    }
                    if (r.message.aod && !frm.doc.aod) {
                        frm.set_value('aod', r.message.aod);
                    }
                    if (r.message.etd && !frm.doc.etd) {
                        frm.set_value('etd', r.message.etd);
                    }
                    if (r.message.eta && !frm.doc.eta) {
                        frm.set_value('eta', r.message.eta);
                    }
                    if (r.message.incoterm && !frm.doc.incoterm) {
                        frm.set_value('incoterm', r.message.incoterm);
                    }
                }
            });
        }
    }
});

// Rate Finder function
function find_rates_for_quotation(frm) {
    // Determine lane type and origin/destination
    let lane_type = null;
    let origin = null;
    let destination = null;
    let mode = null;
    
    if (frm.doc.mode) {
        const modes = frm.doc.mode.split(',');
        mode = modes[0].trim();
        
        if (mode === 'Sea' && frm.doc.pol && frm.doc.pod) {
            lane_type = 'Sea';
            origin = frm.doc.pol;
            destination = frm.doc.pod;
        } else if (mode === 'Air' && frm.doc.aoo && frm.doc.aod) {
            lane_type = 'Air';
            origin = frm.doc.aoo;
            destination = frm.doc.aod;
        } else if (mode === 'Land') {
            lane_type = 'Land';
            frappe.msgprint(__('Land mode rate finder requires origin and destination fields.'));
            return;
        } else {
            frappe.msgprint(__('Please fill in POL/POD for Sea mode or AOO/AOD for Air mode.'));
            return;
        }
    } else {
        frappe.msgprint(__('Please select Mode first.'));
        return;
    }
    
    // Call rate finder API
    frappe.call({
        method: 'freight_forwarding.project.api.find_rates',
        args: {
            lane_type: lane_type,
            origin: origin,
            destination: destination,
            mode: mode,
            date_filter: frm.doc.valid_till || null
        },
        callback: function(r) {
            if (r.message && r.message.length > 0) {
                show_rate_options(frm, r.message);
            } else {
                frappe.msgprint(__('No rates found for this lane.'));
            }
        }
    });
}

// Show rate options dialog
function show_rate_options(frm, rates) {
    let dialog = new frappe.ui.Dialog({
        title: __('Rate Options'),
        fields: [
            {
                fieldtype: 'HTML',
                options: '<div id="rate-options-list"></div>'
            }
        ],
        primary_action_label: __('Apply Selected Rate'),
        primary_action: function() {
            apply_selected_rate(frm, dialog);
        }
    });
    
    // Build rate options HTML
    let html = '<table class="table table-bordered">';
    html += '<thead><tr>';
    html += '<th>Select</th><th>Vendor/Carrier</th><th>Buy Rate</th><th>Sell Rate</th><th>Margin</th><th>Transit</th>';
    html += '</tr></thead><tbody>';
    
    rates.forEach(function(rate, index) {
        html += '<tr>';
        html += '<td><input type="radio" name="selected_rate" value="' + index + '"></td>';
        html += '<td>' + (rate.carrier || rate.vendor || '') + '</td>';
        html += '<td>' + format_currency(rate.buy_rate, rate.currency) + '</td>';
        html += '<td>' + format_currency(rate.sell_rate, rate.currency) + '</td>';
        html += '<td>' + (rate.margin_percent ? rate.margin_percent.toFixed(2) + '%' : '-') + '</td>';
        html += '<td>' + (rate.transit_days || '-') + ' days</td>';
        html += '</tr>';
    });
    
    html += '</tbody></table>';
    
    dialog.fields_dict['rate-options-list'].$wrapper.html(html);
    
    dialog.show();
    
    // Store rates for later use
    dialog.rates = rates;
}

// Apply selected rate to quotation items
function apply_selected_rate(frm, dialog) {
    let selected = dialog.$wrapper.find('input[name="selected_rate"]:checked').val();
    
    if (!selected) {
        frappe.msgprint(__('Please select a rate option.'));
        return;
    }
    
    let rate = dialog.rates[parseInt(selected)];
    
    // Add or update items in quotation
    if (!frm.doc.items || frm.doc.items.length === 0) {
        // Create new item
        let item_row = frm.add_child('items');
        item_row.item_code = 'Freight Service'; // Default item
        item_row.item_name = 'Freight Service';
        item_row.rate = rate.sell_rate;
        item_row.qty = 1;
        item_row.amount = rate.sell_rate;
    } else {
        // Update first item with rate
        let first_item = frm.doc.items[0];
        first_item.rate = rate.sell_rate;
        first_item.amount = first_item.qty * rate.sell_rate;
    }
    
    frm.refresh_field('items');
    dialog.hide();
    
    frappe.msgprint({
        title: __('Success'),
        message: __('Rate applied to quotation. Buy Rate: {0}, Sell Rate: {1}', [
            format_currency(rate.buy_rate, rate.currency),
            format_currency(rate.sell_rate, rate.currency)
        ]),
        indicator: 'green'
    });
}

function format_currency(amount, currency) {
    if (!amount) return '-';
    currency = currency || 'USD';
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency
    }).format(amount);
}

