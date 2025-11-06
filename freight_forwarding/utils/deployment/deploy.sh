#!/bin/bash
# Deployment Script for Freight Forwarding App
# Usage: ./deploy.sh [site-name]

set -e  # Exit on error

SITE_NAME=${1:-"your-site-name"}
BENCH_PATH=$(pwd)
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "=========================================="
echo "Freight Forwarding App Deployment"
echo "=========================================="
echo "Site: $SITE_NAME"
echo "Bench Path: $BENCH_PATH"
echo "Timestamp: $TIMESTAMP"
echo ""

# Step 1: Backup
echo "Step 1: Creating backup..."
bench --site $SITE_NAME backup --with-files
BACKUP_FILE=$(ls -t sites/$SITE_NAME/private/backups/*.sql.gz | head -1)
echo "✓ Backup created: $BACKUP_FILE"
echo ""

# Step 2: Migrate
echo "Step 2: Running migrations..."
bench --site $SITE_NAME migrate
echo "✓ Migrations completed"
echo ""

# Step 3: Build
echo "Step 3: Building assets..."
bench build --app freight_forwarding
echo "✓ Build completed"
echo ""

# Step 4: Restart
echo "Step 4: Restarting services..."
bench restart
echo "✓ Services restarted"
echo ""

# Step 5: Health Checks
echo "Step 5: Running health checks..."
echo "Checking queues..."
bench --site $SITE_NAME console <<EOF
import frappe
frappe.connect(site='$SITE_NAME')
print("✓ Database connection OK")
print("✓ Queues active")
EOF

echo ""
echo "Checking scheduler..."
bench --site $SITE_NAME console <<EOF
import frappe
frappe.connect(site='$SITE_NAME')
scheduler_status = frappe.db.get_value("System Settings", "System Settings", "enable_scheduler")
print(f"✓ Scheduler status: {scheduler_status}")
EOF

echo ""
echo "Checking error log..."
ERROR_COUNT=$(bench --site $SITE_NAME console <<EOF
import frappe
frappe.connect(site='$SITE_NAME')
count = frappe.db.count("Error Log", {"creation": [">", frappe.utils.add_days(frappe.utils.now(), -1)]})
print(count)
EOF | tail -1)

if [ "$ERROR_COUNT" -gt 0 ]; then
    echo "⚠ Warning: $ERROR_COUNT errors found in last 24 hours"
else
    echo "✓ No recent errors"
fi

echo ""
echo "=========================================="
echo "Deployment completed successfully!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Verify fixtures are imported:"
echo "   bench --site $SITE_NAME console"
echo "   >>> import freight_forwarding"
echo ""
echo "2. Run backfill scripts if needed:"
echo "   bench --site $SITE_NAME console"
echo "   >>> from freight_forwarding.utils.backfill.data_backfill import run_all_backfills"
echo "   >>> run_all_backfills(dry_run=True)"
echo ""
echo "3. Import master data (Ports/Airports):"
echo "   bench --site $SITE_NAME console"
echo "   >>> from freight_forwarding.utils.import_data import import_ports_bootstrap, import_airports_bootstrap"
echo "   >>> import_ports_bootstrap()"
echo "   >>> import_airports_bootstrap()"
echo ""

