// Auto-fill division from Project (if project is linked via reference)
frappe.ui.form.on('Payment Entry', {
    refresh: function(frm) {
        // Payment Entry doesn't have direct project field
        // Division should be set from linked document (SI/PI) if available
        // This is a placeholder for future enhancement
    }
});

