#!/bin/bash
# Rollback Script for Freight Forwarding App
# Usage: ./rollback.sh [site-name] [backup-file]

set -e  # Exit on error

SITE_NAME=${1:-"your-site-name"}
BACKUP_FILE=${2:-""}

if [ -z "$BACKUP_FILE" ]; then
    echo "Error: Backup file required"
    echo "Usage: ./rollback.sh [site-name] [backup-file.sql.gz]"
    echo ""
    echo "Available backups:"
    ls -t sites/$SITE_NAME/private/backups/*.sql.gz 2>/dev/null | head -5
    exit 1
fi

echo "=========================================="
echo "Freight Forwarding App Rollback"
echo "=========================================="
echo "Site: $SITE_NAME"
echo "Backup File: $BACKUP_FILE"
echo ""
echo "⚠ WARNING: This will restore the database from backup!"
echo "Press Ctrl+C to cancel, or Enter to continue..."
read

# Step 1: Stop services
echo "Step 1: Stopping services..."
bench restart --stop
echo "✓ Services stopped"
echo ""

# Step 2: Restore database
echo "Step 2: Restoring database..."
bench --site $SITE_NAME restore $BACKUP_FILE --with-public-files --with-private-files
echo "✓ Database restored"
echo ""

# Step 3: Restart services
echo "Step 3: Restarting services..."
bench restart
echo "✓ Services restarted"
echo ""

echo "=========================================="
echo "Rollback completed!"
echo "=========================================="

