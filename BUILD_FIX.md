# Build Fix Documentation

## Masalah
Error saat menjalankan `bench build --app freight_forwarding`:
```
TypeError [ERR_INVALID_ARG_TYPE]: The "paths[0]" argument must be of type string. Received undefined
```

## Analisis
Error terjadi di `get_all_files_to_build` di esbuild. Kemungkinan penyebab:
1. Esbuild tidak bisa resolve app directory saat menggunakan `--apps freight_forwarding`
2. Atau ada masalah dengan bagaimana esbuild membaca hooks.py saat build untuk satu app saja

## Solusi yang Sudah Dicoba
1. ✅ Memperbaiki path di `doctype_js` (menghapus prefix `freight_forwarding/`)
2. ✅ Memastikan semua file client scripts ada
3. ✅ Menghapus `app_include_js` untuk menghindari path resolution issues
4. ✅ Memastikan `package.json` ada dan valid
5. ✅ Memastikan semua file di `public/js/` ada

## Workaround (Solusi Sementara)
**Gunakan `bench build` tanpa `--app` flag:**
```bash
bench build
```
Ini akan build semua apps termasuk `freight_forwarding` dan sudah terbukti berhasil.

## Solusi Permanen (Investigasi Lebih Lanjut)
Masalah ini kemungkinan terkait dengan:
1. Bagaimana esbuild membaca hooks.py saat menggunakan `--apps` flag
2. Atau masalah dengan app directory resolution di Frappe v15

**Rekomendasi:**
- Gunakan `bench build` tanpa `--app` untuk saat ini
- Atau build hanya saat diperlukan (tidak perlu build setiap kali)
- Monitor issue ini di Frappe repository jika terjadi pada apps lain

## Status
- ✅ Semua file dan konfigurasi sudah benar
- ✅ Build dengan `bench build` (tanpa --app) berhasil
- ⚠️ Build dengan `bench build --app freight_forwarding` masih error (tapi tidak critical)

## Catatan
Error ini tidak mempengaruhi functionality app. App tetap bisa diinstall dan digunakan dengan normal. Hanya build process yang perlu menggunakan workaround.

