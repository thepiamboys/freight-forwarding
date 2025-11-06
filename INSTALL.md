# Installation Guide

## Prerequisites

- Bench installed and configured
- Frappe Framework v15.x
- ERPNext v15.x
- Python 3.10.x
- Node.js 18 LTS

## Installation Steps

### Option 1: Install from Local Directory

1. Navigate to your bench directory:
```bash
cd /path/to/your/bench
```

2. Get the app from local directory:
```bash
bench get-app freight_forwarding /Users/mac/Desktop/DEV/Freightforwading
```

3. Install the app on your site:
```bash
bench --site [your-site-name] install-app freight_forwarding
```

4. Run migrations:
```bash
bench --site [your-site-name] migrate
```

5. Build assets:
```bash
bench build --app freight_forwarding
bench restart
```

### Option 2: Install from Git Repository

1. Get the app from repository:
```bash
bench get-app freight_forwarding https://github.com/your-org/freight_forwarding
```

2. Install the app:
```bash
bench --site [your-site-name] install-app freight_forwarding
bench --site [your-site-name] migrate
bench build --app freight_forwarding
bench restart
```

## Verification

After installation, verify the app is installed:

```bash
bench --site [your-site-name] list-apps
```

You should see `freight_forwarding` in the list.

## Post-Installation

After installation, follow the migration order as specified in the main README.md:

1. Item Group tree → Default accounts
2. Tax templates & Tax Rule 1.1%
3. Custom Doctypes
4. Custom Fields & Property Setters
5. Server Scripts
6. Import FF Port/Airport CSV
7. Reports
8. UI enhancements
9. Rate Management
10. Data backfill

## Troubleshooting

If you encounter issues:

1. Check bench logs:
```bash
bench --site [your-site-name] logs
```

2. Verify app structure:
```bash
ls freight_forwarding/
```

3. Rebuild assets:
```bash
bench build --app freight_forwarding
bench restart
```

