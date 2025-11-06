// Project Client Script
// Adds Tab Finance with embedded lists

frappe.ui.form.on('Project', {
    refresh: function(frm) {
        // Add Tab Finance if not already added
        if (!frm.tabs_dict['finance']) {
            frm.add_custom_button(__('Finance'), function() {
                show_finance_tab(frm);
            }, __('View'));
        }
        
        // Add Finance tab to form
        if (frm.doc.name && !frm.tabs_dict['finance_tab']) {
            add_finance_tab(frm);
        }
    }
});

function add_finance_tab(frm) {
    // Create Finance tab
    let finance_tab = frm.add_tab('finance_tab', __('Finance'));
    
    // Add HTML section for lists
    let html = `
        <div class="finance-tab-content" style="padding: 15px;">
            <div class="row">
                <div class="col-md-6">
                    <h5>${__('Employee Advances')}</h5>
                    <div id="employee_advances_list"></div>
                    <button class="btn btn-sm btn-primary" onclick="frappe.set_route('Form', 'Employee Advance', {project: '${frm.doc.name}'})">
                        ${__('New Employee Advance')}
                    </button>
                    <a href="/app/employee-advance?project=${encodeURIComponent(frm.doc.name)}" class="btn btn-sm btn-default">
                        ${__('View All')}
                    </a>
                </div>
                <div class="col-md-6">
                    <h5>${__('Expense Claims')}</h5>
                    <div id="expense_claims_list"></div>
                    <button class="btn btn-sm btn-primary" onclick="frappe.set_route('Form', 'Expense Claim', {project: '${frm.doc.name}'})">
                        ${__('New Expense Claim')}
                    </button>
                    <a href="/app/expense-claim?project=${encodeURIComponent(frm.doc.name)}" class="btn btn-sm btn-default">
                        ${__('View All')}
                    </a>
                </div>
            </div>
            <div class="row" style="margin-top: 20px;">
                <div class="col-md-6">
                    <h5>${__('Purchase Orders')}</h5>
                    <div id="purchase_orders_list"></div>
                    <button class="btn btn-sm btn-primary" onclick="frappe.set_route('Form', 'Purchase Order', {project: '${frm.doc.name}'})">
                        ${__('New Purchase Order')}
                    </button>
                    <a href="/app/purchase-order?project=${encodeURIComponent(frm.doc.name)}" class="btn btn-sm btn-default">
                        ${__('View All')}
                    </a>
                </div>
                <div class="col-md-6">
                    <h5>${__('Purchase Invoices')}</h5>
                    <div id="purchase_invoices_list"></div>
                    <button class="btn btn-sm btn-primary" onclick="frappe.set_route('Form', 'Purchase Invoice', {project: '${frm.doc.name}'})">
                        ${__('New Purchase Invoice')}
                    </button>
                    <a href="/app/purchase-invoice?project=${encodeURIComponent(frm.doc.name)}" class="btn btn-sm btn-default">
                        ${__('View All')}
                    </a>
                </div>
            </div>
            <div class="row" style="margin-top: 20px;">
                <div class="col-md-6">
                    <h5>${__('Sales Invoices')}</h5>
                    <div id="sales_invoices_list"></div>
                    <button class="btn btn-sm btn-primary" onclick="frappe.set_route('Form', 'Sales Invoice', {project: '${frm.doc.name}'})">
                        ${__('New Sales Invoice')}
                    </button>
                    <a href="/app/sales-invoice?project=${encodeURIComponent(frm.doc.name)}" class="btn btn-sm btn-default">
                        ${__('View All')}
                    </a>
                </div>
                <div class="col-md-6">
                    <h5>${__('Payment Entries')}</h5>
                    <div id="payment_entries_list"></div>
                    <button class="btn btn-sm btn-primary" onclick="frappe.set_route('Form', 'Payment Entry', {project: '${frm.doc.name}'})">
                        ${__('New Payment Entry')}
                    </button>
                    <a href="/app/payment-entry?project=${encodeURIComponent(frm.doc.name)}" class="btn btn-sm btn-default">
                        ${__('View All')}
                    </a>
                </div>
            </div>
        </div>
    `;
    
    $(finance_tab).html(html);
    
    // Load lists
    load_finance_lists(frm);
}

function load_finance_lists(frm) {
    if (!frm.doc.name) return;
    
    // Load Employee Advances
    frappe.call({
        method: 'freight_forwarding.project.api.list_by_project',
        args: {
            doctype: 'Employee Advance',
            project: frm.doc.name,
            fields: 'name,status,posting_date,advance_amount',
            limit: 5
        },
        callback: function(r) {
            if (r.message) {
                render_list('employee_advances_list', r.message, 'Employee Advance');
            }
        }
    });
    
    // Load Expense Claims
    frappe.call({
        method: 'freight_forwarding.project.api.list_by_project',
        args: {
            doctype: 'Expense Claim',
            project: frm.doc.name,
            fields: 'name,status,expense_date,total_claimed_amount',
            limit: 5
        },
        callback: function(r) {
            if (r.message) {
                render_list('expense_claims_list', r.message, 'Expense Claim');
            }
        }
    });
    
    // Load Purchase Orders
    frappe.call({
        method: 'freight_forwarding.project.api.list_by_project',
        args: {
            doctype: 'Purchase Order',
            project: frm.doc.name,
            fields: 'name,status,transaction_date,grand_total',
            limit: 5
        },
        callback: function(r) {
            if (r.message) {
                render_list('purchase_orders_list', r.message, 'Purchase Order');
            }
        }
    });
    
    // Load Purchase Invoices
    frappe.call({
        method: 'freight_forwarding.project.api.list_by_project',
        args: {
            doctype: 'Purchase Invoice',
            project: frm.doc.name,
            fields: 'name,status,posting_date,grand_total',
            limit: 5
        },
        callback: function(r) {
            if (r.message) {
                render_list('purchase_invoices_list', r.message, 'Purchase Invoice');
            }
        }
    });
    
    // Load Sales Invoices
    frappe.call({
        method: 'freight_forwarding.project.api.list_by_project',
        args: {
            doctype: 'Sales Invoice',
            project: frm.doc.name,
            fields: 'name,status,posting_date,grand_total',
            limit: 5
        },
        callback: function(r) {
            if (r.message) {
                render_list('sales_invoices_list', r.message, 'Sales Invoice');
            }
        }
    });
    
    // Load Payment Entries
    frappe.call({
        method: 'freight_forwarding.project.api.list_by_project',
        args: {
            doctype: 'Payment Entry',
            project: frm.doc.name,
            fields: 'name,status,posting_date,paid_amount',
            limit: 5
        },
        callback: function(r) {
            if (r.message) {
                render_list('payment_entries_list', r.message, 'Payment Entry');
            }
        }
    });
}

function render_list(container_id, items, doctype) {
    let container = $(`#${container_id}`);
    if (!container.length) return;
    
    if (!items || items.length === 0) {
        container.html('<p class="text-muted">' + __('No records found') + '</p>');
        return;
    }
    
    let html = '<ul class="list-unstyled">';
    items.forEach(function(item) {
        html += `<li style="padding: 5px 0;">
            <a href="/app/${doctype.toLowerCase().replace(/\s+/g, '-')}/${item.name}" class="text-muted">
                ${item.name}
            </a>
            <span class="label label-default">${item.status || ''}</span>
        </li>`;
    });
    html += '</ul>';
    
    container.html(html);
}

function show_finance_tab(frm) {
    // Switch to finance tab if exists
    if (frm.tabs_dict['finance_tab']) {
        frm.set_active_tab('finance_tab');
    } else {
        add_finance_tab(frm);
    }
}

