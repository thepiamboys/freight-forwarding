// Auto-fill division from Project (from first expense detail)
frappe.ui.form.on('Expense Claim', {
    refresh: function(frm) {
        // Set division from first expense detail's project
        if (frm.doc.expenses && frm.doc.expenses.length > 0) {
            const first_expense = frm.doc.expenses[0];
            if (first_expense.project && !frm.doc.division) {
                frappe.db.get_value('Project', first_expense.project, 'division').then(r => {
                    const division = r.message && r.message.division;
                    if (division) {
                        frm.set_value('division', division);
                    }
                });
            }
        }
    }
});

// Auto-set service_type from Item Group on Expense Claim Detail
frappe.ui.form.on('Expense Claim Detail', {
    item_code: function(frm, cdt, cdn) {
        const row = locals[cdt][cdn];
        if (!row.item_code) return;

        frappe.db.get_value('Item', row.item_code, 'item_group').then(r => {
            const item_group = r.message && r.message.item_group;
            if (item_group) {
                const service_type = infer_service_type(item_group);
                if (service_type && !row.service_type) {
                    frappe.model.set_value(cdt, cdn, 'service_type', service_type);
                }
            }
        });
    },

    project: function(frm, cdt, cdn) {
        const row = locals[cdt][cdn];
        if (!row.project) return;

        // Update header division if not set
        if (!frm.doc.division) {
            frappe.db.get_value('Project', row.project, 'division').then(r => {
                const division = r.message && r.message.division;
                if (division) {
                    frm.set_value('division', division);
                }
            });
        }
    }
});

function infer_service_type(item_group) {
    const map = {
        'Freight': 'Freight',
        'Customs': 'Customs',
        'Trucking': 'Trucking',
        'Port': 'Port',
        'Warehouse': 'Warehouse',
        'Surcharges': 'Surcharges'
    };

    if (map[item_group]) {
        return map[item_group];
    }

    if (item_group && item_group.includes('Freight Services')) {
        const parts = item_group.split('/');
        for (let part of parts) {
            if (map[part.trim()]) {
                return map[part.trim()];
            }
        }
    }

    return null;
}

