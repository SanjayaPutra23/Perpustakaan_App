import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime, timedelta
from backup_restore import backup_database, restore_database

LOAN_DURATION_DAYS = 7 

class DashboardFrame(ttk.Frame):
    def __init__(self, parent, controller, style_instance):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = self.controller.db
        self.style = style_instance 

        # --- Definisi Styles ---
        self.style.configure("DashboardTitle.TLabel", font=("Arial", 18, "bold"), foreground="#007BFF")
        self.style.configure("Summary.TLabel", font=("Arial", 12), foreground="#333333")
        self.style.configure("Dashboard.TLabelframe.Label", font=("Arial", 11, "bold"), foreground="#333333")
        self.style.configure("Dashboard.TLabelframe", background="#F8F8F8", relief="solid", borderwidth=1)

        # Ini akan menimpa default dari ttkthemes, tapi lebih stabil
        self.style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#DDDDDD", foreground="#333333")
        self.style.configure("Treeview", rowheight=25, font=("Arial", 9))
        self.style.map('Treeview', background=[('selected', '#B0C4DE')])


        self.style.configure("DBUtil.TButton", 
                             font=("Arial", 10, "bold"),
                             padding=8,
                             background="#6C757D",
                             foreground="black",
                             relief="flat")
        self.style.map("DBUtil.TButton",
                       background=[('active', '#5A6268')])

        self.style.configure('Dashboard.TButton', 
                             font=('Arial', 11, 'bold'),
                             padding=10,
                             background='#4CAF50',
                             foreground='black',
                             relief='flat')
        self.style.map('Dashboard.TButton',
                       background=[('active', '#66BB6A')])

        self.style.configure('Logout.TButton', 
                             font=('Arial', 10, 'bold'),
                             background='#DC3545',
                             foreground='black')
        self.style.map('Logout.TButton',
                       background=[('active', '#C82333')])


        # Frame untuk Judul dan Tombol Logout
        header_frame = ttk.Frame(self, padding="15 10")
        header_frame.pack(pady=10, padx=10, fill="x")

        lbl_title = ttk.Label(header_frame, text="Dashboard Admin 🏠", style="DashboardTitle.TLabel")
        lbl_title.pack(side=tk.LEFT, expand=True)

        btn_logout = ttk.Button(header_frame, text="🚪 Logout", command=self.controller.logout, style='Logout.TButton')
        btn_logout.pack(side=tk.RIGHT)

        # Frame untuk menampilkan ringkasan data
        summary_frame = ttk.LabelFrame(self, text="📊 Ringkasan Data Perpustakaan", style="Dashboard.TLabelframe")
        summary_frame.pack(pady=5, padx=20, fill="x")

        self.lbl_total_books = ttk.Label(summary_frame, text="Total Buku: -", style="Summary.TLabel")
        self.lbl_total_books.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.lbl_available_books = ttk.Label(summary_frame, text="Buku Tersedia: -", style="Summary.TLabel")
        self.lbl_available_books.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.lbl_total_members = ttk.Label(summary_frame, text="Total Anggota: -", style="Summary.TLabel")
        self.lbl_total_members.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.lbl_active_borrowings = ttk.Label(summary_frame, text="Peminjaman Aktif: -", style="Summary.TLabel")
        self.lbl_active_borrowings.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        summary_frame.grid_columnconfigure(0, weight=1)
        summary_frame.grid_columnconfigure(1, weight=1)

        # Frame untuk Notifikasi Keterlambatan
        self.overdue_frame = ttk.LabelFrame(self, text="❗ Notifikasi Keterlambatan Pengembalian", style="Dashboard.TLabelframe")
        self.overdue_frame.pack(pady=5, padx=20, fill="both", expand=True)

        scrollbar_y_overdue = ttk.Scrollbar(self.overdue_frame, orient=tk.VERTICAL)
        scrollbar_x_overdue = ttk.Scrollbar(self.overdue_frame, orient=tk.HORIZONTAL)

        # Gunakan style="Treeview" (style default)
        self.tree_overdue = ttk.Treeview(self.overdue_frame,
                                         columns=("Judul Buku", "Nama Anggota", "Tgl Pinjam", "Jatuh Tempo", "Hari Terlambat"),
                                         show="headings",
                                         yscrollcommand=scrollbar_y_overdue.set,
                                         xscrollcommand=scrollbar_x_overdue.set,
                                         style="Treeview")

        # Konfigurasi tag untuk Treeview, harus setelah Treeview dibuat
        self.tree_overdue.tag_configure('critical_overdue', foreground='red', font=('Arial', 9, 'bold'))

        scrollbar_y_overdue.config(command=self.tree_overdue.yview)
        scrollbar_x_overdue.config(command=self.tree_overdue.xview)
        self.tree_overdue.heading("Judul Buku", text="Judul Buku")
        self.tree_overdue.heading("Nama Anggota", text="Nama Anggota")
        self.tree_overdue.heading("Tgl Pinjam", text="Tgl Pinjam")
        self.tree_overdue.heading("Jatuh Tempo", text="Jatuh Tempo")
        self.tree_overdue.heading("Hari Terlambat", text="Hari Terlambat")
        self.tree_overdue.column("Judul Buku", width=200)
        self.tree_overdue.column("Nama Anggota", width=150)
        self.tree_overdue.column("Tgl Pinjam", width=100, anchor="center")
        self.tree_overdue.column("Jatuh Tempo", width=100, anchor="center")
        self.tree_overdue.column("Hari Terlambat", width=100, anchor="center")
        self.tree_overdue.grid(row=0, column=0, sticky="nsew")
        scrollbar_y_overdue.grid(row=0, column=1, sticky="ns")
        scrollbar_x_overdue.grid(row=1, column=0, sticky="ew")
        self.overdue_frame.grid_rowconfigure(0, weight=1)
        self.overdue_frame.grid_columnconfigure(0, weight=1)

        # Frame untuk Utilitas Database (Backup/Restore)
        db_utils_frame = ttk.LabelFrame(self, text="🗄️ Utilitas Database", style="Dashboard.TLabelframe")
        db_utils_frame.pack(pady=5, padx=20, fill="x")

        btn_backup_db = ttk.Button(db_utils_frame, text="💾 Backup Database", command=self.perform_backup, style="DBUtil.TButton")
        btn_backup_db.pack(side=tk.LEFT, padx=10, pady=5)

        btn_restore_db = ttk.Button(db_utils_frame, text="🔄 Restore Database", command=self.perform_restore, style="DBUtil.TButton")
        btn_restore_db.pack(side=tk.LEFT, padx=10, pady=5)


        # Frame untuk tombol navigasi di Dashboard
        nav_button_frame = ttk.Frame(self)
        nav_button_frame.pack(pady=15, padx=20, fill="x")

        nav_button_frame.grid_columnconfigure(0, weight=1)
        nav_button_frame.grid_columnconfigure(1, weight=1)
        nav_button_frame.grid_columnconfigure(2, weight=1)
        nav_button_frame.grid_columnconfigure(3, weight=1)

        btn_manage_books = ttk.Button(nav_button_frame, text="📚 Manajemen Buku",
                                      command=lambda: self.controller.show_frame("ManajemenBuku"),
                                      style='Dashboard.TButton')
        btn_manage_books.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        btn_manage_members = ttk.Button(nav_button_frame, text="👥 Manajemen Anggota",
                                        command=lambda: self.controller.show_frame("ManajemenAnggota"),
                                        style='Dashboard.TButton')
        btn_manage_members.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        btn_manage_borrowings = ttk.Button(nav_button_frame, text="📤 Peminjaman & Pengembalian",
                                           command=lambda: self.controller.show_frame("ManajemenPeminjaman"),
                                           style='Dashboard.TButton')
        btn_manage_borrowings.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        btn_reports = ttk.Button(nav_button_frame, text="📊 Laporan",
                                 command=lambda: self.controller.show_frame("Laporan"),
                                 style='Dashboard.TButton')
        btn_reports.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        self.load_dashboard_data()

    def perform_backup(self):
        try:
            if self.db and self.db.conn:
                self.db.disconnect()
                print("Koneksi database ditutup sebelum backup.")

            backup_database()
            messagebox.showinfo("Backup Database", "Database berhasil di-backup. ✅")
        except Exception as e:
            messagebox.showerror("Error Backup", f"Gagal mem-backup database: {e} ❌")
        finally:
            if self.db and not self.db.conn:
                self.db.connect()
                print("Koneksi database disambungkan kembali setelah backup.")

    def perform_restore(self):
        if messagebox.askyesno("Konfirmasi Restore", "Anda yakin ingin me-restore database? Ini akan menimpa data saat ini. Pastikan Anda sudah mem-backup data penting!"):
            try:
                if self.db and self.db.conn:
                    self.db.disconnect()
                    print("Koneksi database ditutup sebelum restore.")
                
                restore_database()
                messagebox.showinfo("Restore Selesai", "Proses restore telah dijalankan. "
                                     "Sangat disarankan untuk me-restart aplikasi "
                                     "agar semua perubahan diterapkan dengan benar. ✔️")
                self.controller.root.quit()
            except Exception as e:
                messagebox.showerror("Error Restore", f"Gagal me-restore database: {e} ❌")
            finally:
                if self.db and not self.db.conn:
                    self.db.connect()
                    print("Koneksi database disambungkan kembali setelah restore.")

    def load_dashboard_data(self):
        try:
            if not self.db or not self.db.conn or not self.db.cursor:
                print("Koneksi database tidak aktif, mencoba menyambungkan ulang...")
                self.db.connect()
                if not self.db.conn:
                    messagebox.showerror("Error Database", "Koneksi ke database gagal. Tidak dapat memuat data dashboard.")
                    return

            self.db.cursor.execute("SELECT COUNT(*) FROM books")
            total_books = self.db.cursor.fetchone()[0]
            self.lbl_total_books.config(text=f"Total Buku: {total_books} 📚")

            self.db.cursor.execute("SELECT SUM(available) FROM books")
            available_books = self.db.cursor.fetchone()[0]
            if available_books is None: available_books = 0
            self.lbl_available_books.config(text=f"Buku Tersedia: {available_books} ✅")

            self.db.cursor.execute("SELECT COUNT(*) FROM members")
            total_members = self.db.cursor.fetchone()[0]
            self.lbl_total_members.config(text=f"Total Anggota: {total_members} 🧑‍🤝‍🧑")

            self.db.cursor.execute("SELECT COUNT(*) FROM borrowings WHERE status = 'Borrowed'")
            active_borrowings = self.db.cursor.fetchone()[0]
            self.lbl_active_borrowings.config(text=f"Peminjaman Aktif: {active_borrowings} 📖")

        except Exception as e:
            messagebox.showerror("Error Database", f"Gagal memuat data ringkasan dashboard: {e} ⚠️")
            for lbl in [self.lbl_total_books, self.lbl_available_books, self.lbl_total_members, self.lbl_active_borrowings]:
                current_text = lbl.cget("text").split(":")[0]
                lbl.config(text=f"{current_text}: Error ❌")
        self.load_overdue_notifications()

    def load_overdue_notifications(self):
        for item in self.tree_overdue.get_children():
            self.tree_overdue.delete(item)
        try:
            if not self.db or not self.db.conn or not self.db.cursor:
                print("Koneksi database tidak aktif untuk notifikasi keterlambatan.")
                if hasattr(self, 'overdue_frame'):
                    self.overdue_frame.config(text="❗ Notifikasi Keterlambatan Pengembalian (DB tidak aktif)")
                return

            self.db.cursor.execute("""
                SELECT bo.title, m.name, b.borrow_date
                FROM borrowings b
                JOIN books bo ON b.book_id = bo.id
                JOIN members m ON b.member_id = m.id
                WHERE b.status = 'Borrowed'
            """)
            borrowed_items = self.db.cursor.fetchall()
            today = datetime.now().date()
            overdue_count = 0
            
            loan_duration = LOAN_DURATION_DAYS

            for item_data in borrowed_items:
                book_title, member_name, borrow_date_str = item_data
                borrow_date_dt = datetime.strptime(borrow_date_str, "%Y-%m-%d").date()
                due_date_dt = borrow_date_dt + timedelta(days=loan_duration)
                if due_date_dt < today:
                    days_overdue = (today - due_date_dt).days
                    display_values = (book_title, member_name, borrow_date_str, due_date_dt.strftime("%Y-%m-%d"), f"{days_overdue} hari")
                    self.tree_overdue.insert("", tk.END, values=display_values, tags=('critical_overdue',))
                    overdue_count += 1

            if hasattr(self, 'overdue_frame'):
                self.overdue_frame.config(text=f"❗ Notifikasi Keterlambatan Pengembalian ({overdue_count} buku terlambat)")
            else:
                print("Warning: self.overdue_frame attribute not found, cannot update text.")

        except Exception as e:
            messagebox.showerror("Error Database", f"Gagal memuat notifikasi keterlambatan: {e} ⚠️")
            if hasattr(self, 'overdue_frame'):
                self.overdue_frame.config(text="❗ Notifikasi Keterlambatan Pengembalian (Error Memuat)")

    def on_show(self):
        print("Dashboard frame shown. Loading data...")
        self.load_dashboard_data()