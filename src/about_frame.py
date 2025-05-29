import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class AboutFrame(ttk.Frame):
    # Parameter style_instance harus diterima dari main.py
    def __init__(self, parent, controller, style_instance):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Gunakan instance style global dari main.py
        self.style = style_instance 

        # --- Definisi Style Menggunakan self.style (Global) ---
        # Gaya untuk Label Judul
        self.style.configure("AboutTitle.TLabel", 
                              font=("Arial", 22, "bold"), 
                              foreground="#00796B") # Warna hijau tua
        # Catatan: Emotikon di teks akan ditampilkan oleh Tkinter/OS, bukan style

        # Gaya untuk LabelFrame "Informasi Aplikasi"
        self.style.configure("AboutInfo.TLabelframe.Label", 
                              font=("Arial", 11, "bold"), 
                              foreground="#333333") # Abu-abu gelap
        self.style.configure("AboutInfo.TLabelframe", 
                              background="#F8F8F8", # Latar belakang LabelFrame
                              relief="groove", # Memberi sedikit kedalaman
                              borderwidth=2) # Border lebih tebal

        # Gaya untuk label info (teks normal)
        self.style.configure("AboutInfo.TLabel", font=("Arial", 11))
        # Gaya untuk label info (teks bold)
        self.style.configure("AboutInfoBold.TLabel", 
                              font=("Arial", 11, "bold"), 
                              foreground="#424242") # Abu-abu gelap

        # Gaya khusus untuk tombol Kembali
        self.style.configure("AboutBack.TButton", 
                                    font=("Arial", 12, "bold"), 
                                    foreground="black", # Teks hitam
                                    background="#4CAF50", # Warna hijau daun
                                    padding=10,
                                    relief="raised") 
        self.style.map("AboutBack.TButton", 
                                    background=[('active', '#66BB6A')]) # Hijau lebih terang saat di-hover
        # --- Akhir Definisi Style ---

        # Frame untuk Judul
        title_frame = ttk.Frame(self)
        title_frame.pack(pady=25)
        
        # Gunakan style yang sudah didefinisikan dengan self.style
        lbl_title = ttk.Label(title_frame, text="✨ Tentang Aplikasi Perpustakaan ✨", style="AboutTitle.TLabel")
        lbl_title.pack()

        # Frame untuk Konten Info
        # Gunakan style yang sudah didefinisikan dengan self.style
        info_frame = ttk.LabelFrame(self, text="Informasi Aplikasi", padding=(20, 10), style="AboutInfo.TLabelframe")
        info_frame.pack(pady=15, padx=30, fill="x", expand=False)

        row_idx = 0
        
        # Gunakan style yang sudah didefinisikan dengan self.style
        ttk.Label(info_frame, text="Nama Aplikasi:", style="AboutInfoBold.TLabel").grid(row=row_idx, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(info_frame, text="Sistem Informasi Perpustakaan Digital", style="AboutInfo.TLabel").grid(row=row_idx, column=1, sticky="w", padx=5, pady=2)
        row_idx += 1

        ttk.Label(info_frame, text="Versi:", style="AboutInfoBold.TLabel").grid(row=row_idx, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(info_frame, text="📚 1.0.0 (Stabil)", style="AboutInfo.TLabel").grid(row=row_idx, column=1, sticky="w", padx=5, pady=2)
        row_idx += 1

        ttk.Label(info_frame, text="Pengembang:", style="AboutInfoBold.TLabel").grid(row=row_idx, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(info_frame, text="🧑‍💻 KELOMPOK 8 (Sanjaya, Ayu Rianti, Muhammad Abdullah Fikri)", style="AboutInfo.TLabel").grid(row=row_idx, column=1, sticky="w", padx=5, pady=2)
        row_idx += 1

        ttk.Label(info_frame, text="Lisensi:", style="AboutInfoBold.TLabel").grid(row=row_idx, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(info_frame, text="📄 Open Source (MIT License)", style="AboutInfo.TLabel").grid(row=row_idx, column=1, sticky="w", padx=5, pady=2)
        row_idx += 1

        ttk.Label(info_frame, text="Dibangun dengan:", style="AboutInfoBold.TLabel").grid(row=row_idx, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(info_frame, text="🐍 Python, Tkinter, ttkthemes, SQLite, ReportLab", style="AboutInfo.TLabel").grid(row=row_idx, column=1, sticky="w", padx=5, pady=2)
        row_idx += 1

        ttk.Label(info_frame, text="Kontak:", style="AboutInfoBold.TLabel").grid(row=row_idx, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(info_frame, text="📧 sanjayaonekidz@gmail.com", style="AboutInfo.TLabel").grid(row=row_idx, column=1, sticky="w", padx=5, pady=2)
        row_idx += 1

        ttk.Label(info_frame, text="Hak Cipta:", style="AboutInfoBold.TLabel").grid(row=row_idx, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(info_frame, text="© 2025 Kelompok 8. All rights reserved.", style="AboutInfo.TLabel").grid(row=row_idx, column=1, sticky="w", padx=5, pady=2)
        row_idx += 1

        info_frame.grid_columnconfigure(1, weight=1)

        # Tombol Kembali
        # Gunakan style yang sudah didefinisikan dengan self.style
        btn_back = ttk.Button(self, text="⬅️ Kembali ke Dashboard", command=self.back_to_appropriate_dashboard, style="AboutBack.TButton")
        btn_back.pack(pady=30)


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
        print("About frame shown.")