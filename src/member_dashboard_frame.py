import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime, timedelta
from database import FINE_PER_DAY

LOAN_DURATION_DAYS = 7

class MemberDashboardFrame(ttk.Frame):
    def __init__(self, parent, controller, style_instance):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = self.controller.db
        self.member_details = None

        self.style = style_instance 

        # --- Style Configuration (PASTIKAN SEMUA DEFINISI STYLE DI SINI) ---
        # Style untuk Label Judul
        self.style.configure("Header.TLabel", font=("Arial", 18, "bold"), foreground="#333333")
        self.style.configure("MemberName.TLabel", font=("Arial", 12, "italic"), foreground="#555555")

        # Style untuk Treeview (Buku Dipinjam dan Buku Tersedia)
        self.style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#DDDDDD", foreground="#333333") # Warna header gelap
        self.style.configure("Treeview", rowheight=25, font=("Arial", 9)) 
        self.style.map('Treeview', background=[('selected', '#B0C4DE')])

        # Style untuk Button Peminjaman
        self.style.configure("Borrow.TButton",
                             font=("Arial", 11, "bold"),
                             background="#4CAF50",
                             foreground="black",
                             padding=10)
        self.style.map("Borrow.TButton",
                       background=[('active', '#5CB85C')],
                       foreground=[('disabled', '#AAAAAA')])

        # Style untuk tombol navigasi footer
        self.style.configure("Footer.TButton", font=("Arial", 10, "bold"),
                             background="#007BFF", foreground="black",
                             padding="8 5")
        self.style.map("Footer.TButton",
                       background=[('active', '#0056b3')])


        # Frame untuk Judul dan Nama Anggota
        header_frame = ttk.Frame(self, padding="15 10")
        header_frame.pack(pady=10, padx=10, fill="x")

        lbl_title = ttk.Label(header_frame, text="Dashboard Anggota 🏠", style="Header.TLabel")
        lbl_title.pack(side=tk.LEFT, expand=True)

        self.lbl_member_name = ttk.Label(header_frame, text="Selamat Datang, [Nama Anggota]", style="MemberName.TLabel")
        self.lbl_member_name.pack(side=tk.RIGHT)

        # Frame untuk Daftar Buku yang Sedang Dipinjam
        borrowed_books_frame = ttk.LabelFrame(self, text="📚 Buku yang Sedang Anda Pinjam")
        borrowed_books_frame.pack(pady=5, padx=10, fill="both", expand=True)

        # Scrollbar untuk Treeview Buku Dipinjam
        scrollbar_y_borrowed = ttk.Scrollbar(borrowed_books_frame, orient=tk.VERTICAL)
        scrollbar_x_borrowed = ttk.Scrollbar(borrowed_books_frame, orient=tk.HORIZONTAL)

        self.tree_borrowed_books = ttk.Treeview(borrowed_books_frame,
                                                columns=("Judul Buku", "Pengarang", "Tgl Pinjam", "Jatuh Tempo", "Tgl Kembali", "Status", "Denda"),
                                                show="headings",
                                                yscrollcommand=scrollbar_y_borrowed.set,
                                                xscrollcommand=scrollbar_x_borrowed.set,
                                                style="Treeview")

        scrollbar_y_borrowed.config(command=self.tree_borrowed_books.yview)
        scrollbar_x_borrowed.config(command=self.tree_borrowed_books.xview)

        self.tree_borrowed_books.heading("Judul Buku", text="Judul Buku")
        self.tree_borrowed_books.heading("Pengarang", text="Pengarang")
        self.tree_borrowed_books.heading("Tgl Pinjam", text="Tgl Pinjam")
        self.tree_borrowed_books.heading("Jatuh Tempo", text="Jatuh Tempo")
        self.tree_borrowed_books.heading("Tgl Kembali", text="Tgl Kembali")
        self.tree_borrowed_books.heading("Status", text="Status")
        self.tree_borrowed_books.heading("Denda", text="Denda")

        self.tree_borrowed_books.column("Judul Buku", width=200)
        self.tree_borrowed_books.column("Pengarang", width=150)
        self.tree_borrowed_books.column("Tgl Pinjam", width=90, anchor="center")
        self.tree_borrowed_books.column("Jatuh Tempo", width=90, anchor="center")
        self.tree_borrowed_books.column("Tgl Kembali", width=90, anchor="center")
        self.tree_borrowed_books.column("Status", width=100, anchor="center")
        self.tree_borrowed_books.column("Denda", width=80, anchor="e")

        self.tree_borrowed_books.grid(row=0, column=0, sticky="nsew")
        scrollbar_y_borrowed.grid(row=0, column=1, sticky="ns")
        scrollbar_x_borrowed.grid(row=1, column=0, sticky="ew")

        borrowed_books_frame.grid_rowconfigure(0, weight=1)
        borrowed_books_frame.grid_columnconfigure(0, weight=1)

        self.tree_borrowed_books.tag_configure('overdue_borrowed', foreground='red', font=('Arial', 9, 'bold'))
        self.tree_borrowed_books.tag_configure('borrowed', foreground='blue')
        self.tree_borrowed_books.tag_configure('returned', foreground='green')

        # Frame untuk Tombol Aksi Buku Tersedia
        available_books_button_frame = ttk.Frame(self, padding="5 0")
        available_books_button_frame.pack(pady=5, fill="x")

        # Tombol Ajukan Peminjaman Buku Terpilih
        self.btn_request_borrow = ttk.Button(available_books_button_frame,
                                             text="✨ Ajukan Peminjaman Buku Terpilih",
                                             command=self.request_borrowing,
                                             state=tk.DISABLED,
                                             style="Borrow.TButton")
        self.btn_request_borrow.pack(side=tk.RIGHT, padx=5)

        # Tambahkan fungsi pencarian dan tombol refresh
        search_frame = ttk.Frame(available_books_button_frame)
        search_frame.pack(side=tk.LEFT, padx=5)

        ttk.Label(search_frame, text="Cari Buku:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<Return>", lambda event: self.perform_search())
        
        ttk.Button(search_frame, text="🔍 Cari", command=self.perform_search).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="🔄 Segarkan", command=self.load_available_books).pack(side=tk.LEFT, padx=5)


        # Frame untuk Daftar Buku yang Tersedia
        available_books_frame = ttk.LabelFrame(self, text="📚 Buku yang Tersedia untuk Dipinjam")
        available_books_frame.pack(pady=5, padx=10, fill="both", expand=True)

        # Scrollbar untuk Treeview Buku Tersedia
        scrollbar_y_available = ttk.Scrollbar(available_books_frame, orient=tk.VERTICAL)
        scrollbar_x_available = ttk.Scrollbar(available_books_frame, orient=tk.HORIZONTAL)

        self.tree_available_books = ttk.Treeview(available_books_frame,
                                                 columns=("ID", "Judul Buku", "Pengarang", "ISBN", "Kategori", "Tersedia"),
                                                 show="headings",
                                                 yscrollcommand=scrollbar_y_available.set,
                                                 xscrollcommand=scrollbar_x_available.set,
                                                 style="Treeview")

        scrollbar_y_available.config(command=self.tree_available_books.yview)
        scrollbar_x_available.config(command=self.tree_available_books.xview)

        # Define headings
        self.tree_available_books.heading("ID", text="ID")
        self.tree_available_books.heading("Judul Buku", text="Judul Buku")
        self.tree_available_books.heading("Pengarang", text="Pengarang")
        self.tree_available_books.heading("ISBN", text="ISBN")
        self.tree_available_books.heading("Kategori", text="Kategori")
        self.tree_available_books.heading("Tersedia", text="Tersedia")

        # Define column widths
        self.tree_available_books.column("ID", width=50, anchor="center")
        self.tree_available_books.column("Judul Buku", width=200)
        self.tree_available_books.column("Pengarang", width=150)
        self.tree_available_books.column("ISBN", width=100)
        self.tree_available_books.column("Kategori", width=100)
        self.tree_available_books.column("Tersedia", width=70, anchor="center")

        self.tree_available_books.grid(row=0, column=0, sticky="nsew")
        scrollbar_y_available.grid(row=0, column=1, sticky="ns")
        scrollbar_x_available.grid(row=1, column=0, sticky="ew")

        available_books_frame.grid_rowconfigure(0, weight=1)
        available_books_frame.grid_columnconfigure(0, weight=1)

        self.tree_available_books.bind("<<TreeviewSelect>>", self.on_available_book_select)

        # Footer atau navigasi tambahan
        footer_frame = ttk.Frame(self, padding="10 5")
        footer_frame.pack(side=tk.BOTTOM, fill="x", pady=10, padx=10)

        # Tombol Profil
        btn_profile = ttk.Button(footer_frame, text="👤 Profil Saya",
                                 command=lambda: self.controller.show_frame("PengaturanProfil"),
                                 style="Footer.TButton")
        btn_profile.pack(side=tk.LEFT, padx=5)

        # Tombol Logout
        btn_logout = ttk.Button(footer_frame, text="🚪 Logout",
                                command=self.controller.logout,
                                style="Footer.TButton")
        btn_logout.pack(side=tk.RIGHT, padx=5)


    def load_member_data(self):
        member_id = self.controller.current_member_id
        if member_id is None:
            self.lbl_member_name.config(text="Selamat Datang, [Anggota Tidak Dikenal]")
            self.member_details = None
            return
        try:
            self.db.cursor.execute("SELECT id, name, address, phone, email FROM members WHERE id = ?", (member_id,))
            self.member_details = self.db.cursor.fetchone()
            if self.member_details:
                member_id, member_name, address, phone, email = self.member_details
                self.lbl_member_name.config(text=f"Selamat Datang, {member_name} 👋")
            else:
                self.lbl_member_name.config(text="Selamat Datang, [Data Anggota Tidak Ditemukan]")
                self.member_details = None
        except Exception as e:
            messagebox.showerror("Error Database", f"Gagal memuat data anggota: {e}")
            self.lbl_member_name.config(text="Selamat Datang, [Error Memuat Data]")
            self.member_details = None

    def load_borrowed_books(self):
        for item in self.tree_borrowed_books.get_children():
            self.tree_borrowed_books.delete(item)
        if self.member_details is None:
            return
        member_id = self.member_details[0]
        try:
            self.db.cursor.execute("""
                SELECT bo.title, bo.author, b.borrow_date, b.return_date, b.status, b.fine_amount
                FROM borrowings b
                JOIN books bo ON b.book_id = bo.id
                WHERE b.member_id = ?
                ORDER BY CASE b.status WHEN 'Borrowed' THEN 1 ELSE 2 END, b.borrow_date DESC
            """, (member_id,))
            borrowings = self.db.cursor.fetchall()
            today = datetime.now().date()
            for borrowing_item in borrowings:
                book_title, author, borrow_date_str, return_date_str, status, fine_amount = borrowing_item
                borrow_date_dt = datetime.strptime(borrow_date_str, "%Y-%m-%d").date()
                due_date_dt = borrow_date_dt + timedelta(days=LOAN_DURATION_DAYS)
                due_date_str = due_date_dt.strftime("%Y-%m-%d")
                display_status = status
                current_tags = ()
                display_fine = f"Rp {fine_amount:,.0f}" if fine_amount and fine_amount > 0 else "-"
                if status == 'Borrowed':
                    if due_date_dt < today:
                        days_overdue = (today - due_date_dt).days
                        display_status = f"Terlambat ({ days_overdue } hari) ❗"
                        current_tags = ('overdue_borrowed',)
                    else:
                        current_tags = ('borrowed',)
                elif status == 'Returned':
                    current_tags = ('returned',)
                display_values = (book_title, author, borrow_date_str, due_date_str, return_date_str if return_date_str else "", display_status, display_fine)
                self.tree_borrowed_books.insert("", tk.END, values=display_values, tags=current_tags)
        except Exception as e:
            messagebox.showerror("Error Database", f"Gagal memuat daftar buku pinjaman: {e}")

    def load_available_books(self):
        for item in self.tree_available_books.get_children():
            self.tree_available_books.delete(item)
        try:
            search_term = self.search_entry.get().strip()
            if search_term:
                query = """
                    SELECT id, title, author, isbn, category, available
                    FROM books
                    WHERE available > 0
                    AND (title LIKE ? OR author LIKE ? OR isbn LIKE ? OR category LIKE ?)
                    ORDER BY title ASC
                """
                self.db.cursor.execute(query, ('%'+search_term+'%', '%'+search_term+'%', '%'+search_term+'%', '%'+search_term+'%'))
            else:
                query = "SELECT id, title, author, isbn, category, available FROM books WHERE available > 0 ORDER BY title ASC"
                self.db.cursor.execute(query)

            available_books = self.db.cursor.fetchall()
            for book in available_books:
                self.tree_available_books.insert("", tk.END, values=book)
        except Exception as e:
            messagebox.showerror("Error Database", f"Gagal memuat daftar buku tersedia: {e}")

    def perform_search(self):
        self.load_available_books()


    def on_available_book_select(self, event):
        selected_item = self.tree_available_books.focus()
        if selected_item:
            if self.member_details is not None:
                 self.btn_request_borrow.config(state=tk.NORMAL)
            else:
                 self.btn_request_borrow.config(state=tk.DISABLED)
        else:
             self.btn_request_borrow.config(state=tk.DISABLED)

    def request_borrowing(self):
        selected_item = self.tree_available_books.focus()
        if not selected_item:
            messagebox.showwarning("Pilih Buku", "Pilih buku dari daftar yang tersedia untuk dipinjam.")
            return
        if self.member_details is None:
            messagebox.showerror("Error", "Data anggota tidak ditemukan. Silakan logout dan login kembali.")
            return
        book_values = self.tree_available_books.item(selected_item, 'values')
        book_id = book_values[0]
        book_title = book_values[1]
        
        try:
            available_stock = int(book_values[5])
        except ValueError:
            messagebox.showerror("Error Data", "Data stok buku tidak valid. Mohon hubungi administrator.")
            return
        
        if available_stock <= 0:
            messagebox.showwarning("Stok Habis", f"Buku '{book_title}' sudah tidak tersedia.")
            self.load_available_books()
            self.btn_request_borrow.config(state=tk.DISABLED)
            return
        member_id = self.member_details[0]
        member_name = self.member_details[1]

        confirm = messagebox.askyesno("Konfirmasi Peminjaman", f"Anda yakin ingin meminjam buku '{book_title}'?")
        if confirm:
            try:
                borrow_date_dt = datetime.now()
                borrow_date_str = borrow_date_dt.strftime("%Y-%m-%d")
                self.db.cursor.execute("""
                    INSERT INTO borrowings (book_id, member_id, borrow_date, status, fine_amount)
                    VALUES (?, ?, ?, ?, ?)
                """, (book_id, member_id, borrow_date_str, 'Borrowed', 0.0))
                self.db.cursor.execute("""
                    UPDATE books
                    SET available = available - 1
                    WHERE id = ?
                """, (book_id,))
                self.db.conn.commit()
                messagebox.showinfo("Sukses", f"Peminjaman buku '{book_title}' berhasil dicatat. Selamat membaca! 😊")
                self.load_borrowed_books()
                self.load_available_books()
                self.btn_request_borrow.config(state=tk.DISABLED)
            except Exception as e:
                messagebox.showerror("Error Database", f"Gagal memproses peminjaman: {e}")
                self.db.conn.rollback()

    def on_show(self):
        print("Member Dashboard frame shown. Loading data...")
        self.load_member_data()
        self.load_borrowed_books()
        self.load_available_books()
        self.btn_request_borrow.config(state=tk.DISABLED)