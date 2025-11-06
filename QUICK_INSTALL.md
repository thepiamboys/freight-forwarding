# Quick Install Guide

## Error: App not in apps.txt

Jika Anda mendapat error `App freight_forwarding not in apps.txt`, ikuti langkah berikut:

### Solusi Cepat

**Di bench environment, jalankan:**

```bash
# 1. Tambahkan app ke apps.txt
echo "freight_forwarding" >> /workspace/frappe-bench/apps.txt

# 2. Verifikasi
cat /workspace/frappe-bench/apps.txt
# Should show: frappe, erpnext, freight_forwarding

# 3. Install app
bench --site frappe.kurhanz.com install-app freight_forwarding

# 4. Run migrations
bench --site frappe.kurhanz.com migrate

# 5. Build assets
bench build

# 6. Restart
bench restart
```

### Atau Gunakan bench get-app (Recommended)

Jika app belum di-clone, gunakan `bench get-app` yang otomatis menambahkan ke apps.txt:

```bash
# Get app dari GitHub (otomatis menambahkan ke apps.txt)
bench get-app freight_forwarding https://github.com/thepiamboys/freight-forwarding.git

# Install app
bench --site frappe.kurhanz.com install-app freight_forwarding

# Run migrations
bench --site frappe.kurhanz.com migrate

# Build assets
bench build

# Restart
bench restart
```

### Verifikasi

Setelah install, verifikasi app terinstall:

```bash
# List installed apps
bench --site frappe.kurhanz.com list-apps

# Should show: frappe, erpnext, freight_forwarding
```

### Troubleshooting

**Jika apps.txt tidak ada:**
```bash
# Create apps.txt dengan default apps
echo -e "frappe\nerpnext" > /workspace/frappe-bench/apps.txt
echo "freight_forwarding" >> /workspace/frappe-bench/apps.txt
```

**Jika app sudah di-clone tapi tidak di apps.txt:**
```bash
# Check if app exists
ls -la /workspace/frappe-bench/apps/freight_forwarding

# Add to apps.txt
echo "freight_forwarding" >> /workspace/frappe-bench/apps.txt
```

### Catatan

- `apps.txt` berisi daftar semua apps yang terinstall di bench
- `bench get-app` otomatis menambahkan app ke `apps.txt`
- `bench install-app` hanya bekerja jika app sudah ada di `apps.txt`

