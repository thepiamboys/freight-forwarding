# Deployment Guide

## Pre-Deployment Checklist

- [ ] Code review completed
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Database backup scheduled
- [ ] Maintenance window scheduled
- [ ] Team notified

## Deployment Steps

### 1. Backup

```bash
bench --site [site-name] backup --with-files
```

### 2. Migrate

```bash
bench --site [site-name] migrate
```

### 3. Build

```bash
bench build --app freight_forwarding
```

### 4. Restart

```bash
bench restart
```

### 5. Health Checks

```bash
# Check queues
bench --site [site-name] console
>>> import frappe
>>> frappe.connect()
>>> print("OK")

# Check scheduler
>>> scheduler_status = frappe.db.get_value("System Settings", "System Settings", "enable_scheduler")
>>> print(scheduler_status)

# Check error log
>>> error_count = frappe.db.count("Error Log", {"creation": [">", frappe.utils.add_days(frappe.utils.now(), -1)]})
>>> print(error_count)
```

## Automated Deployment

Use the deployment script:

```bash
chmod +x freight_forwarding/utils/deployment/deploy.sh
./freight_forwarding/utils/deployment/deploy.sh [site-name]
```

## Post-Deployment

### 1. Verify Fixtures

```bash
bench --site [site-name] console
>>> import freight_forwarding
>>> # Should import without errors
```

### 2. Import Master Data (if needed)

```bash
bench --site [site-name] console
>>> from freight_forwarding.utils.import_data import import_ports_bootstrap, import_airports_bootstrap
>>> import_ports_bootstrap()
>>> import_airports_bootstrap()
```

### 3. Run Backfill Scripts (if needed)

```bash
bench --site [site-name] console
>>> from freight_forwarding.utils.backfill.data_backfill import run_all_backfills
>>> result = run_all_backfills(dry_run=True)
>>> print(result)
>>> # Review results, then run:
>>> run_all_backfills(dry_run=False)
```

### 4. Verify Custom Fields

Check that custom fields are present:
- Project: division, mode, service_scope, pol, pod, aoo, aod, etd, eta, incoterm
- Sales Invoice: division
- Purchase Invoice: division
- Purchase Order: project, division
- Employee Advance: division, advance_lines
- Expense Claim: division
- Expense Claim Detail: project, item, service_type, advance_ref, advance_line_ref
- Payment Entry: division
- Opportunity: division, mode, service_scope, pol, pod, aoo, aod, etd, eta, incoterm
- Quotation: division, mode, service_scope, pol, pod, aoo, aod, etd, eta, incoterm

### 5. Verify Custom DocTypes

Check that custom doctypes exist:
- FF Port
- FF Airport
- Advance Line

### 6. Verify Reports

Check that reports are available:
- Project Service Breakdown
- Expense Claim Breakdown
- Advance Utilization
- PO Commit vs Actual
- Project Financial Snapshot

### 7. Verify Roles

Check that custom roles exist:
- FF-OPS
- FF-DOCS
- FF-SALES
- FF-FIN
- FF-MANAGER
- FF-ADMIN

## Rollback Procedure

If deployment fails, rollback using:

```bash
chmod +x freight_forwarding/utils/deployment/rollback.sh
./freight_forwarding/utils/deployment/rollback.sh [site-name] [backup-file.sql.gz]
```

Or manually:

```bash
# 1. Stop services
bench restart --stop

# 2. Restore backup
bench --site [site-name] restore [backup-file.sql.gz] --with-public-files --with-private-files

# 3. Restart services
bench restart
```

## Troubleshooting

### Migration Errors

```bash
# Check migration status
bench --site [site-name] migrate --skip-search-index

# Rebuild search index
bench --site [site-name] build --app freight_forwarding
```

### Build Errors

```bash
# Clear cache
bench clear-cache

# Rebuild
bench build --app freight_forwarding
```

### Permission Errors

```bash
# Check permissions
bench --site [site-name] console
>>> import frappe
>>> frappe.connect()
>>> frappe.get_roles()
```

## Production Deployment

For production deployments:

1. **Schedule maintenance window**
2. **Notify users**
3. **Create full backup** (database + files)
4. **Deploy during low-traffic period**
5. **Monitor error logs** for 24 hours
6. **Verify critical workflows**
7. **Update documentation**

## Health Monitoring

After deployment, monitor:

- Error Log (Setup → Error Log)
- Queue status (Setup → Background Jobs)
- Scheduler status (Setup → Scheduler)
- System performance
- User feedback

## Support

For issues or questions:
- Check error logs
- Review deployment logs
- Contact development team
- Refer to INSTALL.md for installation issues

