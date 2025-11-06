// Auto-fill division from Project
frappe.ui.form.on('Employee Advance', {
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

