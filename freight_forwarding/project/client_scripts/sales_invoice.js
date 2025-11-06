// Auto-fill division from Project
frappe.ui.form.on('Sales Invoice', {
    project: function(frm) {
        if (!frm.doc.project) {
            frm.set_value('division', '');
            return;
        }

        frappe.db.get_value('Project', frm.doc.project, 'division').then(r => {
            const division = r.message && r.message.division;
            if (division) {
                frm.set_value('division', division);
            }
        });
    }
});

// Auto-set service_type from Item Group
frappe.ui.form.on('Sales Invoice Item', {
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

    // Check direct match
    if (map[item_group]) {
        return map[item_group];
    }

    // Check if item_group is under Freight Services
    if (item_group && item_group.includes('Freight Services')) {
        // Try to extract service type from path
        const parts = item_group.split('/');
        for (let part of parts) {
            if (map[part.trim()]) {
                return map[part.trim()];
            }
        }
    }

    return null;
}

