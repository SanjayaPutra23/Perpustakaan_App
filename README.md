# APLIKASI MANAJEMEN PERPUSTAKAAN BERBASIS PYTHON

## Anggota Kelompok 8
- **Sanjaya** (230511039)
- **Ayu Rianti** (230511037)
- **Muhammad Abdullah Fikri** (230511048)  
**Kelas:** TI23B

## Deskripsi Aplikasi
Aplikasi manajemen perpustakaan berbasis GUI Python dengan database SQLite untuk mengelola:
- Data buku (tambah, edit, hapus, cari)
- Data anggota perpustakaan
- Transaksi peminjaman dan pengembalian buku
- Generate laporan dalam format PDF

## Teknologi yang Digunakan
| Komponen         | Teknologi/Library       |
|------------------|-------------------------|
| Bahasa Pemrogram | Python 3.6+             |
| Database         | SQLite                  |
| GUI Framework    | Tkinter                 |
| Library Tambahan | reportlab, ttkthemes    |

## Persyaratan Sistem
- Python 3.6 atau versi lebih baru
- pip (Python package installer)

## Panduan Instalasi & Menjalankan Aplikasi

### 1. Clone Repository
```bash
git clone https://github.com/SanjayaPutra23/Perpustakaan_App.git
cd Perpustakaan_App
```

### 2. Setup Virtual Environment (Direkomendasikan)
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependensi
```bash
pip install reportlab ttkthemes
```

### 4. Menjalankan Aplikasi
```bash
python library_app/main.py
```

## Akses Login
### Untuk Admin :
```bash
🔑 Username: admin
🔒 Password: admin123
```
### Untuk User/Anggota :
```bash
🔑 Username: sanjaya
🔒 Password: sanjaya123

🔑 Username: ayurianti
🔒 Password: ayu123

🔑 Username: fikri
🔒 Password: fikri123
```

## Library yang digunakan
### Library Bawaan Python:
- **tkinter** (untuk antarmuka GUI)
- **sqlite3** (untuk database)
- **datetime** (manajemen waktu)
- **hashlib** (enkripsi password)
- **os** (operasi sistem file)

### Library Eksternal :
- **reportlab** (generator PDF)
- **ttkthemes** (tema modern untuk GUI)

## Troubleshooting
- ❌ Masalah: ModuleNotFoundError
- ✅ Solusi: Pastikan semua dependensi terinstal dengan pip install -r requirements.txt

- ❌ Masalah: Database error
- ✅ Solusi: Tutup aplikasi lain yang mungkin mengakses database

- ❌ Masalah: Tampilan GUI tidak proporsional
- ✅ Solusi: Gunakan resolusi layar minimal 1366x768