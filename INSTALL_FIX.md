# Fix: App not in apps.txt Error

## Error Message
```
App freight_forwarding not in apps.txt
```

## Cause
The app needs to be added to `apps.txt` file in your bench before it can be installed.

## Solution

### Option 1: Use `bench get-app` (Recommended)

If you haven't cloned the app yet, use `bench get-app` which automatically adds it to `apps.txt`:

```bash
# From your bench directory
cd /workspace/frappe-bench

# Get app from GitHub
bench get-app freight_forwarding https://github.com/thepiamboys/freight-forwarding.git

# Then install
bench --site frappe.kurhanz.com install-app freight_forwarding
```

### Option 2: Manual Add to apps.txt

If the app is already cloned but not in `apps.txt`:

```bash
# 1. Navigate to bench directory
cd /workspace/frappe-bench

# 2. Add app to apps.txt
echo "freight_forwarding" >> apps.txt

# 3. Verify it's added
cat apps.txt

# 4. Now install the app
bench --site frappe.kurhanz.com install-app freight_forwarding
```

### Option 3: If App is Already Cloned

If you already have the app in `apps/` folder but it's not in `apps.txt`:

```bash
# 1. Check if app exists
ls -la apps/freight_forwarding

# 2. Add to apps.txt
echo "freight_forwarding" >> apps.txt

# 3. Install
bench --site frappe.kurhanz.com install-app freight_forwarding
```

## Complete Installation Steps

```bash
# 1. Get app (if not already cloned)
bench get-app freight_forwarding https://github.com/thepiamboys/freight-forwarding.git

# 2. Install app
bench --site frappe.kurhanz.com install-app freight_forwarding

# 3. Run migrations
bench --site frappe.kurhanz.com migrate

# 4. Build assets
bench build --app freight_forwarding

# 5. Restart bench
bench restart
```

## Verification

After installation, verify the app is installed:

```bash
# List installed apps
bench --site frappe.kurhanz.com list-apps

# You should see 'freight_forwarding' in the list
```

## Troubleshooting

### If apps.txt doesn't exist:
```bash
# Create apps.txt with default apps
echo -e "frappe\nerpnext" > apps.txt
echo "freight_forwarding" >> apps.txt
```

### If app is in wrong location:
```bash
# Make sure app is in apps/ directory
ls -la apps/freight_forwarding

# If not, move it
mv /path/to/freight_forwarding apps/
```

### Check bench structure:
```bash
# Your bench should have this structure:
# /workspace/frappe-bench/
#   ├── apps/
#   │   ├── frappe/
#   │   ├── erpnext/
#   │   └── freight_forwarding/  <-- App should be here
#   ├── sites/
#   └── apps.txt  <-- Should contain app names
```

