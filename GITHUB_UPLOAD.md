# Upload ke GitHub

Repository sudah siap untuk di-upload ke GitHub!

## Status
✅ Git repository initialized
✅ All files committed (124 files, 11,689+ lines)
✅ Branch renamed to `main`

## Langkah-langkah Upload

### 1. Buat Repository di GitHub

1. Login ke [GitHub.com](https://github.com)
2. Klik tombol **"+"** di kanan atas → **"New repository"**
3. Isi informasi:
   - **Repository name**: `freight-forwarding` (atau nama lain yang Anda inginkan)
   - **Description**: `Enterprise-grade Freight Forwarding add-on for ERPNext v15`
   - **Visibility**: Pilih Public atau Private
   - **JANGAN** centang "Initialize with README" (karena sudah ada)
4. Klik **"Create repository"**

### 2. Copy Repository URL

Setelah repository dibuat, GitHub akan menampilkan URL repository. Copy URL tersebut, contoh:
- HTTPS: `https://github.com/USERNAME/freight-forwarding.git`
- SSH: `git@github.com:USERNAME/freight-forwarding.git`

### 3. Upload ke GitHub

Jalankan perintah berikut (ganti `<YOUR_GITHUB_REPO_URL>` dengan URL repository Anda):

```bash
cd /Users/mac/Desktop/DEV/Freightforwading
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```

**Contoh jika menggunakan HTTPS:**
```bash
git remote add origin https://github.com/USERNAME/freight-forwarding.git
git push -u origin main
```

**Contoh jika menggunakan SSH:**
```bash
git remote add origin git@github.com:USERNAME/freight-forwarding.git
git push -u origin main
```

### 4. Verifikasi

Setelah push berhasil, buka repository di GitHub dan pastikan semua file sudah ter-upload.

## Troubleshooting

### Jika ada error authentication:
- Untuk HTTPS: Gunakan Personal Access Token (Settings → Developer settings → Personal access tokens)
- Untuk SSH: Setup SSH key di GitHub (Settings → SSH and GPG keys)

### Jika ingin mengubah remote URL:
```bash
git remote set-url origin <NEW_URL>
```

### Jika ingin melihat remote yang sudah di-set:
```bash
git remote -v
```

## Quick Command (Setelah Repo Dibuat)

Jika repository sudah dibuat dengan nama `freight-forwarding` dan username GitHub Anda adalah `YOUR_USERNAME`, jalankan:

```bash
cd /Users/mac/Desktop/DEV/Freightforwading
git remote add origin https://github.com/YOUR_USERNAME/freight-forwarding.git
git push -u origin main
```

## Catatan

- Semua file sudah di-commit dengan message yang deskriptif
- `.gitignore` sudah dikonfigurasi untuk Frappe/ERPNext project
- Branch utama adalah `main` (bukan `master`)

