# Fix apps.txt

## Masalah

`apps.txt` hanya berisi `freight_forwarding` berulang kali, tapi tidak ada `frappe` dan `erpnext`.

Frappe installer memerlukan `apps.txt` yang berisi semua apps termasuk `frappe` dan `erpnext`.

## Solusi

**Di bench environment, jalankan:**

```bash
# 1. Perbaiki apps.txt dengan semua apps yang diperlukan
echo -e "frappe\nerpnext\nfreight_forwarding" > /workspace/frappe-bench/apps.txt

# 2. Verifikasi
cat /workspace/frappe-bench/apps.txt
# Should show:
# frappe
# erpnext
# freight_forwarding

# 3. Install app
bench --site frappe.kurhanz.com install-app freight_forwarding

# 4. Run migrations
bench --site frappe.kurhanz.com migrate

# 5. Build assets
bench build

# 6. Restart
bench restart
```

## Atau Gunakan sed untuk Membersihkan

Jika ingin membersihkan duplikat dan memastikan format benar:

```bash
# 1. Buat apps.txt yang benar
cat > /workspace/frappe-bench/apps.txt << EOF
frappe
erpnext
freight_forwarding
EOF

# 2. Verifikasi
cat /workspace/frappe-bench/apps.txt

# 3. Install app
bench --site frappe.kurhanz.com install-app freight_forwarding
```

## Verifikasi

Setelah install, verifikasi:

```bash
# List installed apps
bench --site frappe.kurhanz.com list-apps
# Should show: frappe, erpnext, freight_forwarding

# Check apps.txt
cat /workspace/frappe-bench/apps.txt
# Should show:
# frappe
# erpnext
# freight_forwarding
```

## Catatan

- `apps.txt` harus berisi semua apps yang terinstall di bench
- Format: satu app per baris
- `frappe` dan `erpnext` harus ada di `apps.txt`
- Tidak boleh ada duplikat

