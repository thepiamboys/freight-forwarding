// Freight Forwarding App
// Main JavaScript file for client-side functionality
// Client scripts are loaded via hooks.py doctype_js configuration

// This file is required for esbuild to work correctly
frappe.provide('freight_forwarding');

freight_forwarding.init = function() {
    console.log('Freight Forwarding app loaded');
};

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', freight_forwarding.init);
} else {
    freight_forwarding.init();
}
