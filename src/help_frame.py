import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox

class HelpFrame(ttk.Frame):
    def __init__(self, parent, controller, style_instance):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.style = style_instance 

        # Gaya untuk Label Judul
        self.style.configure("HelpTitle.TLabel",
                              font=("Arial", 22, "bold"), 
                              foreground="#00796B") 

        # Gaya untuk Tombol Kembali
        self.style.configure("HelpBack.TButton", 
                             font=("Arial", 11, "bold"),
                             foreground="black",       
                             background="#4CAF50",  
                             padding=10,               
                             relief="flat")     

        # Hover effect untuk Tombol Kembali
        self.style.map("HelpBack.TButton",
                       background=[("active", "#66BB6A")]) 
        # --- Akhir Definisi Styles ---


        # Frame untuk Judul
        title_frame = ttk.Frame(self)
        title_frame.pack(pady=25)
        
        # <<< GUNAKAN self.style dan nama style yang sudah didefinisikan
        lbl_title = ttk.Label(title_frame, text="✨ Bantuan Penggunaan Aplikasi ✨", style="HelpTitle.TLabel")
        lbl_title.pack()

        # Area Teks Bantuan (menggunakan ScrolledText agar bisa di-scroll)
        help_text_frame = ttk.Frame(self)
        help_text_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.help_text_area = scrolledtext.ScrolledText(help_text_frame, wrap=tk.WORD,
                                                        width=80, height=20,
                                                        font=("Arial", 10))
        self.help_text_area.pack(fill="both", expand=True)

        default_help_text = """
Panduan Penggunaan Aplikasi Manajemen Perpustakaan

Selamat datang di Aplikasi Manajemen Perpustakaan. Aplikasi ini membantu Anda mengelola data buku, anggota, dan transaksi peminjaman/pengembalian.

1.  Login: Masukkan username dan password Anda di halaman awal. Gunakan username 'admin' dan password 'adminpassword' untuk pertama kali (disarankan untuk segera menggantinya di Pengaturan Profil).
2.  Dashboard: Setelah login, Anda akan melihat ringkasan data perpustakaan dan notifikasi buku yang terlambat.
3.  Manajemen Buku:
    -   Gunakan form di bagian atas untuk menambah buku baru.
    -   Pilih baris di tabel untuk mengisi form dengan data buku yang ada, lalu gunakan tombol 'Ubah Buku' atau 'Hapus Buku'.
    -   Gunakan field 'Pencarian Buku' untuk mencari buku berdasarkan judul, pengarang, ISBN, atau kategori.
    -   Tombol 'Tampilkan Semua' akan menampilkan kembali seluruh daftar buku.
4.  Manajemen Anggota: Mirip dengan Manajemen Buku, untuk mengelola data anggota perpustakaan.
5.  Peminjaman & Pengembalian:
    -   Gunakan field 'Pilih Anggota' dan 'Pilih Buku' untuk mencari dan memilih anggota serta buku yang akan dipinjam.
    -   Klik 'Proses Peminjaman' untuk mencatat transaksi. Struk peminjaman akan dibuat dalam format PDF.
    -   Pilih baris di tabel 'Daftar Peminjaman' yang berstatus 'Borrowed', lalu klik 'Proses Pengembalian' untuk mencatat pengembalian.
    -   Item yang terlambat dikembalikan akan ditandai.
5.  Laporan:
    -   Pilih rentang tanggal dan status (Semua, Borrowed, Returned) untuk memfilter data peminjaman/pengembalian.
    -   Klik 'Tampilkan Laporan' untuk melihat hasilnya di tabel.
    -   Gunakan tombol 'Ekspor ke CSV' atau 'Ekspor ke PDF' untuk menyimpan laporan.
7.  Pengaturan Profil: Akses dari menu 'Akun' setelah login. Anda bisa mengganti password Anda di sini.
8.  Tentang Aplikasi: Akses dari menu 'Bantuan' untuk melihat informasi versi dan pengembang.

Tips:
-   Pastikan format tanggal yang dimasukkan adalah YYYY-MM-DD.
-   Untuk restore database, pastikan aplikasi ditutup atau koneksi database ditutup sebelum melakukan restore, dan disarankan me-restart aplikasi setelahnya.

Jika Anda mengalami masalah, hubungi administrator sistem.
"""
        self.help_text_area.insert(tk.END, default_help_text)
        self.help_text_area.config(state=tk.DISABLED) 

        # Tombol Kembali
        btn_back = ttk.Button(self,
                              text="🏠 Kembali ke Dashboard",
                              command=self.back_to_appropriate_dashboard,
                              style="HelpBack.TButton")
        btn_back.pack(pady=20)

    def back_to_appropriate_dashboard(self):
        user_role = self.controller.current_user_role

        if user_role == "member":
            self.controller.show_frame("MemberDashboard")
        elif user_role in ["admin", "petugas"]:
            self.controller.show_frame("Dashboard")
        else:
            messagebox.showwarning("Navigasi", "Role pengguna tidak dikenal. Kembali ke halaman login.")
            self.controller.logout()

    def on_show(self):
        print("Help frame shown.")