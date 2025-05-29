import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from datetime import datetime, timedelta
from receipt_generator import generate_borrowing_receipt
from database import FINE_PER_DAY

LOAN_DURATION_DAYS = 7

class BorrowingManagementFrame(ttk.Frame):
    def __init__(self, parent, controller, style_instance): # Ini sudah benar
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = self.controller.db

        # Inisialisasi Style
        self.style = style_instance

        # --- Definisi Styles ---
        # Gaya untuk Judul Frame
        self.style.configure("ManagementTitle.TLabel", font=("Arial", 18, "bold"), foreground="#007BFF") #
        
        # Gaya untuk LabelFrame (box input peminjaman)
        self.style.configure("Input.TLabelframe.Label", font=("Arial", 11, "bold"), foreground="#333333")
        self.style.configure("Input.TLabelframe", background="#F8F8F8", relief="solid", borderwidth=1)

        # Gaya untuk Tombol Pencarian (Cari Anggota, Cari Buku)
        self.style.configure("Search.TButton",
                             font=("Arial", 9, "bold"),
                             background="#17A2B8", 
                             foreground="black",
                             padding="5 3")
        self.style.map("Search.TButton",
                       background=[('active', '#138496')])

        # Gaya untuk Tombol Proses Peminjaman
        self.style.configure("ProcessBorrow.TButton",
                             font=("Arial", 11, "bold"),
                             background="#28A745",
                             foreground="black",
                             padding=10)
        self.style.map("ProcessBorrow.TButton",
                       background=[('active', '#218838')])

        # Gaya untuk Tombol Proses Pengembalian
        self.style.configure("ProcessReturn.TButton",
                             font=("Arial", 11, "bold"),
                             background="#FFC107",
                             foreground="#6C6C6C",
                             padding=10)
        self.style.map("ProcessReturn.TButton",
                       background=[('active', "#0C8A45")])
        # Gaya untuk Label Status (Terpilih)
        self.style.configure("Success.TLabel", foreground="green", font=("Arial", 10, "italic"))
        self.style.configure("Error.TLabel", foreground="red", font=("Arial", 10, "italic"))
        self.style.configure("Warning.TLabel", foreground="orange", font=("Arial", 10, "italic"))

        # Gaya untuk Treeview Header dan Baris
        self.style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#DDDDDD", foreground="#333333")
        self.style.configure("Treeview", rowheight=25, font=("Arial", 9))
        self.style.map('Treeview', background=[('selected', '#B0C4DE')])

        # Frame untuk Judul (TETAP DI SINI)
        title_frame = ttk.Frame(self)
        title_frame.pack(pady=10)
        lbl_title = ttk.Label(title_frame, text="🔄 Manajemen Peminjaman & Pengembalian", style="ManagementTitle.TLabel")
        lbl_title.pack()

        # Frame untuk Input Peminjaman (TETAP DI SINI)
        borrow_input_frame = ttk.LabelFrame(self, text="➕ Input Peminjaman Baru", style="Input.TLabelframe")
        borrow_input_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(borrow_input_frame, text="Pilih Anggota (ID/Nama):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_member = ttk.Entry(borrow_input_frame, width=40)
        self.entry_member.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.btn_find_member = ttk.Button(borrow_input_frame, text="🔍 Cari Anggota", command=self.find_member, style="Search.TButton")
        self.btn_find_member.grid(row=0, column=2, padx=5, pady=5)
        self.lbl_selected_member = ttk.Label(borrow_input_frame, text="")
        self.lbl_selected_member.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        self.selected_member_id = None
        self.selected_member_name = None

        ttk.Label(borrow_input_frame, text="Pilih Buku (ID/Judul/ISBN):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_book = ttk.Entry(borrow_input_frame, width=40)
        self.entry_book.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.btn_find_book = ttk.Button(borrow_input_frame, text="📚 Cari Buku", command=self.find_book, style="Search.TButton")
        self.btn_find_book.grid(row=1, column=2, padx=5, pady=5)
        self.lbl_selected_book = ttk.Label(borrow_input_frame, text="")
        self.lbl_selected_book.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        self.selected_book_id = None
        self.selected_book_title = None

        btn_borrow = ttk.Button(borrow_input_frame, text="🚀 Proses Peminjaman", command=self.process_borrowing, style="ProcessBorrow.TButton")
        btn_borrow.grid(row=2, column=0, columnspan=4, pady=10)

        borrow_input_frame.grid_columnconfigure(1, weight=1)
        borrow_input_frame.grid_columnconfigure(3, weight=1)

        # Frame dan Tabel untuk Menampilkan Data Peminjaman Aktif (Treeview)
        table_frame = ttk.Frame(self)
        table_frame.pack(pady=10, padx=10, fill="both", expand=True)

        scrollbar_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        scrollbar_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)

        self.tree_borrowings = ttk.Treeview(table_frame,
                                            columns=("ID", "Judul Buku", "Nama Anggota", "Tgl Pinjam", "Jatuh Tempo", "Tgl Kembali", "Status", "Denda"),
                                            show="headings",
                                            yscrollcommand=scrollbar_y.set,
                                            xscrollcommand=scrollbar_x.set,
                                            style="Treeview")

        self.tree_borrowings.tag_configure('overdue_borrowed', foreground='red', font=('Arial', 9, 'bold'))
        self.tree_borrowings.tag_configure('borrowed', foreground='blue')
        self.tree_borrowings.tag_configure('returned', foreground='green')

        scrollbar_y.config(command=self.tree_borrowings.yview)
        scrollbar_x.config(command=self.tree_borrowings.xview)

        # Define headings
        self.tree_borrowings.heading("ID", text="ID Pinjam")
        self.tree_borrowings.heading("Judul Buku", text="Judul Buku")
        self.tree_borrowings.heading("Nama Anggota", text="Nama Anggota")
        self.tree_borrowings.heading("Tgl Pinjam", text="Tgl Pinjam")
        self.tree_borrowings.heading("Jatuh Tempo", text="Jatuh Tempo")
        self.tree_borrowings.heading("Tgl Kembali", text="Tgl Kembali")
        self.tree_borrowings.heading("Status", text="Status")
        self.tree_borrowings.heading("Denda", text="Denda")

        # Define column widths
        self.tree_borrowings.column("ID", width=70, anchor="center")
        self.tree_borrowings.column("Judul Buku", width=180)
        self.tree_borrowings.column("Nama Anggota", width=130)
        self.tree_borrowings.column("Tgl Pinjam", width=90, anchor="center")
        self.tree_borrowings.column("Jatuh Tempo", width=90, anchor="center")
        self.tree_borrowings.column("Tgl Kembali", width=90, anchor="center")
        self.tree_borrowings.column("Status", width=80, anchor="center")
        self.tree_borrowings.column("Denda", width=80, anchor="e")

        self.tree_borrowings.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.tree_borrowings.bind("<<TreeviewSelect>>", self.on_borrowing_select)


        # Frame untuk Tombol Pengembalian
        return_button_frame = ttk.Frame(self)
        return_button_frame.pack(pady=10)

        self.btn_return = ttk.Button(return_button_frame, text="✅ Proses Pengembalian", command=self.process_return, state=tk.DISABLED, style="ProcessReturn.TButton")
        self.btn_return.pack()

    def find_member(self):
        search_term = self.entry_member.get()
        if not search_term:
            messagebox.showwarning("Input Kosong", "Masukkan ID atau Nama Anggota untuk mencari.")
            return
        try:
            member = None
            if search_term.isdigit():
                self.db.cursor.execute("SELECT id, name FROM members WHERE id = ?", (int(search_term),))
                member = self.db.cursor.fetchone()
            else:
                self.db.cursor.execute("SELECT id, name FROM members WHERE name LIKE ?", (f"%{search_term}%",))
                members = self.db.cursor.fetchall()
                if len(members) > 1:
                    messagebox.showinfo("Hasil Pencarian", f"Ditemukan {len(members)} anggota. Mengambil yang pertama: {members[0][1]}.")
                    member = members[0]
                elif len(members) == 1:
                    member = members[0]
            
            if member:
                self.selected_member_id = member[0]
                self.selected_member_name = member[1]
                self.lbl_selected_member.config(text=f"Terpilih: {member[1]} (ID: {member[0]})", style="Success.TLabel")
            else:
                self.selected_member_id = None; self.selected_member_name = None
                self.lbl_selected_member.config(text="Anggota tidak ditemukan. ❌", style="Error.TLabel")
                messagebox.showwarning("Tidak Ditemukan", "Anggota dengan ID/Nama tersebut tidak ditemukan.")
        except Exception as e:
            messagebox.showerror("Error Database", f"Gagal mencari anggota: {e}")
            self.selected_member_id = None; self.selected_member_name = None
            self.lbl_selected_member.config(text="Error mencari anggota. ⚠️", style="Error.TLabel")

    def find_book(self):
        search_term = self.entry_book.get()
        if not search_term:
            messagebox.showwarning("Input Kosong", "Masukkan ID, Judul, atau ISBN Buku untuk mencari.")
            return
        try:
            book = None
            if search_term.isdigit():
                self.db.cursor.execute("SELECT id, title, available FROM books WHERE id = ?", (int(search_term),))
                book = self.db.cursor.fetchone()
            else:
                self.db.cursor.execute("SELECT id, title, available FROM books WHERE title LIKE ? OR isbn LIKE ?", (f"%{search_term}%", f"%{search_term}%"))
                books = self.db.cursor.fetchall()
                if len(books) > 1:
                    messagebox.showinfo("Hasil Pencarian", f"Ditemukan {len(books)} buku. Mengambil yang pertama: {books[0][1]}.")
                    book = books[0]
                elif len(books) == 1:
                    book = books[0]

            if book:
                self.selected_book_id = book[0]
                self.selected_book_title = book[1]
                self.lbl_selected_book.config(text=f"Terpilih: {book[1]} (Stok Tersedia: {book[2]})", style="Success.TLabel")
                if book[2] <= 0:
                     self.lbl_selected_book.config(text=f"Terpilih: {book[1]} (Stok Tersedia: {book[2]}) - TIDAK TERSEDIA 🚫", style="Warning.TLabel")
                     self.selected_book_id = None; self.selected_book_title = None
            else:
                self.selected_book_id = None; self.selected_book_title = None
                self.lbl_selected_book.config(text="Buku tidak ditemukan. ❌", style="Error.TLabel")
                messagebox.showwarning("Tidak Ditemukan", "Buku dengan ID/Judul/ISBN tersebut tidak ditemukan.")
        except Exception as e:
            messagebox.showerror("Error Database", f"Gagal mencari buku: {e}")
            self.selected_book_id = None; self.selected_book_title = None
            self.lbl_selected_book.config(text="Error mencari buku. ⚠️", style="Error.TLabel")

    def process_borrowing(self):
        if self.selected_member_id is None or self.selected_book_id is None:
            messagebox.showwarning("Pilihan Kurang", "Pilih anggota dan buku terlebih dahulu.")
            return

        self.db.cursor.execute("SELECT available FROM books WHERE id = ?", (self.selected_book_id,))
        if self.db.cursor.fetchone()[0] <= 0:
            messagebox.showwarning("Stok Habis", "Buku tidak tersedia untuk dipinjam.")
            self.selected_book_id = None; self.selected_book_title = None
            self.lbl_selected_book.config(text="Buku tidak tersedia. 🚫", style="Warning.TLabel")
            return

        try:
            borrow_date_dt = datetime.now()
            borrow_date_str = borrow_date_dt.strftime("%Y-%m-%d")
            due_date_dt = borrow_date_dt + timedelta(days=LOAN_DURATION_DAYS)
            due_date_str = due_date_dt.strftime("%Y-%m-%d")

            self.db.cursor.execute("""
                INSERT INTO borrowings (book_id, member_id, borrow_date, status, fine_amount)
                VALUES (?, ?, ?, ?, ?)
            """, (self.selected_book_id, self.selected_member_id, borrow_date_str, 'Borrowed', 0.0))

            borrowing_id = self.db.cursor.lastrowid

            self.db.cursor.execute("UPDATE books SET available = available - 1 WHERE id = ?", (self.selected_book_id,))
            self.db.conn.commit()
            messagebox.showinfo("Sukses", "Peminjaman berhasil dicatat. Struk peminjaman telah dibuat. 🎉")

            receipt_details = {
                'borrowing_id': borrowing_id,
                'book_title': self.selected_book_title,
                'member_name': self.selected_member_name,
                'borrow_date': borrow_date_str,
                'due_date': due_date_str,
                'library_name': "Perpustakaan Kita"
            }
            generate_borrowing_receipt(receipt_details)

            self.clear_borrow_form()
            self.load_borrowings()
            if "ManajemenBuku" in self.controller.frames and self.controller.frames["ManajemenBuku"].winfo_exists():
                 self.controller.frames["ManajemenBuku"].load_books()
        except Exception as e:
            messagebox.showerror("Error Database", f"Gagal memproses peminjaman: {e}")
            self.db.conn.rollback()

    def process_return(self):
        selected_item_iid = self.tree_borrowings.focus()
        if not selected_item_iid:
            messagebox.showwarning("Pilih Data", "Pilih data peminjaman dari tabel yang ingin dikembalikan.")
            return

        values = self.tree_borrowings.item(selected_item_iid, 'values')
        borrowing_id = values[0]
        borrow_date_str = values[3]
        due_date_str = values[4]
        status = values[6]
        current_fine = values[7]

        if 'Returned' in status:
             messagebox.showwarning("Sudah Dikembalikan", "Buku ini sudah berstatus Dikembalikan. ↩️")
             return

        if messagebox.askyesno("Konfirmasi Pengembalian", f"Yakin ingin memproses pengembalian buku dengan ID Peminjaman {borrowing_id}?"):
            try:
                return_date_dt = datetime.now()
                return_date_str_now = return_date_dt.strftime("%Y-%m-%d")

                calculated_fine = 0.0
                try:
                    borrow_date_dt_obj = datetime.strptime(borrow_date_str, "%Y-%m-%d").date()
                    due_date_dt_obj = datetime.strptime(due_date_str, "%Y-%m-%d").date()
                    return_date_dt_obj = return_date_dt.date()

                    if return_date_dt_obj > due_date_dt_obj:
                        days_overdue = (return_date_dt_obj - due_date_dt_obj).days
                        calculated_fine = days_overdue * FINE_PER_DAY
                        messagebox.showinfo("Denda Terlambat", f"Buku terlambat dikembalikan selama {days_overdue} hari.\nDenda: Rp {calculated_fine:,.0f} 💸")

                except ValueError:
                    print("Error parsing date for fine calculation.")
                
                self.db.cursor.execute("SELECT book_id FROM borrowings WHERE id = ?", (borrowing_id,))
                book_id_result = self.db.cursor.fetchone()
                if not book_id_result:
                    messagebox.showerror("Error", "Tidak dapat menemukan ID buku untuk peminjaman ini.")
                    return
                book_id = book_id_result[0]

                self.db.cursor.execute("""
                    UPDATE borrowings
                    SET return_date = ?, status = ?, fine_amount = ?
                    WHERE id = ?
                """, (return_date_str_now, 'Returned', calculated_fine, borrowing_id))

                self.db.cursor.execute("""
                    UPDATE books
                    SET available = available + 1
                    WHERE id = ?
                """, (book_id,))

                self.db.conn.commit()
                messagebox.showinfo("Sukses", "Pengembalian berhasil dicatat. ✅")
                self.load_borrowings()
                self.btn_return.config(state=tk.DISABLED)
                if "ManajemenBuku" in self.controller.frames and self.controller.frames["ManajemenBuku"].winfo_exists():
                     self.controller.frames["ManajemenBuku"].load_books()

            except Exception as e:
                messagebox.showerror("Error Database", f"Gagal memproses pengembalian: {e}")
                self.db.conn.rollback()

    def load_borrowings(self):
        for item in self.tree_borrowings.get_children():
            self.tree_borrowings.delete(item)
        try:
            self.db.cursor.execute("""
                SELECT b.id, bo.title, m.name, b.borrow_date, b.return_date, b.status, b.fine_amount
                FROM borrowings b
                JOIN books bo ON b.book_id = bo.id
                JOIN members m ON b.member_id = m.id
                ORDER BY CASE b.status WHEN 'Borrowed' THEN 1 ELSE 2 END, b.borrow_date DESC
            """)
            rows = self.db.cursor.fetchall()
            today = datetime.now().date()

            for row_idx, db_row in enumerate(rows):
                borrowing_id, book_title, member_name, borrow_date_str, return_date_str, status, fine_amount = db_row

                borrow_date_dt = datetime.strptime(borrow_date_str, "%Y-%m-%d").date()
                due_date_dt = borrow_date_dt + timedelta(days=LOAN_DURATION_DAYS)
                due_date_str = due_date_dt.strftime("%Y-%m-%d")

                display_status = status
                current_tags = ()
                display_fine = f"Rp {fine_amount:,.0f}" if fine_amount > 0 else "-"

                if status == 'Borrowed':
                    if due_date_dt < today:
                        days_overdue_display = (today - due_date_dt).days
                        display_status = f"Terlambat ({days_overdue_display} hari) 🔴"
                        current_tags = ('overdue_borrowed',)
                    else:
                        current_tags = ('borrowed',)
                elif status == 'Returned':
                    display_status = "Dikembalikan ✔️"
                    current_tags = ('returned',)

                display_values = (borrowing_id, book_title, member_name, borrow_date_str, due_date_str, return_date_str if return_date_str else "", display_status, display_fine)

                self.tree_borrowings.insert("", tk.END, values=display_values, tags=current_tags, iid=f"item_{row_idx}")

        except Exception as e:
            messagebox.showerror("Error Database", f"Gagal memuat data peminjaman: {e}")

    def clear_borrow_form(self):
        self.entry_member.delete(0, tk.END); self.entry_book.delete(0, tk.END)
        self.lbl_selected_member.config(text=""); self.lbl_selected_book.config(text="")
        self.selected_member_id = None; self.selected_member_name = None
        self.selected_book_id = None; self.selected_book_title = None
        if self.tree_borrowings.focus():
            self.tree_borrowings.selection_remove(self.tree_borrowings.focus())
        self.btn_return.config(state=tk.DISABLED)

    def on_borrowing_select(self, event):
        selected_item_iid = self.tree_borrowings.focus()
        if selected_item_iid:
            values = self.tree_borrowings.item(selected_item_iid, 'values')
            status_display = values[6]

            if 'Borrowed' in status_display or 'Terlambat' in status_display:
                 self.btn_return.config(state=tk.NORMAL)
            else:
                 self.btn_return.config(state=tk.DISABLED)
        else:
             self.btn_return.config(state=tk.DISABLED)

    def on_show(self):
        print("Borrowing Management frame shown. Loading borrowings...")
        self.load_borrowings()
        self.clear_borrow_form()