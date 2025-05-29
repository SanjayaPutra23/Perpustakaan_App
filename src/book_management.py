import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class BookManagementFrame(ttk.Frame):
    # <<< __init__ SEKARANG MENERIMA style_instance
    def __init__(self, parent, controller, style_instance):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = self.controller.db

        self.style = style_instance 
        # Gaya untuk Judul Frame
        self.style.configure("ManagementTitle.TLabel", font=("Arial", 18, "bold"), foreground="#1a5276") # Biru tua
        
        # Gaya untuk LabelFrame (box detail buku & pencarian)
        self.style.configure("Detail.TLabelframe.Label", font=("Arial", 11, "bold"), foreground="#333333")
        self.style.configure("Detail.TLabelframe", background="#F5F5F5", relief="solid", borderwidth=1)

        # Gaya untuk Tombol Aksi (Tambah, Ubah, Hapus, Bersihkan)
        self.style.configure("Action.TButton",
                             font=("Arial", 10, "bold"),
                             padding=8,
                             relief="flat")

        # Gaya khusus untuk tombol Tambah (hijau cerah, teks putih)
        self.style.configure("Add.Action.TButton",
                             background="#2ECC71",
                             foreground="black")
        self.style.map("Add.Action.TButton",
                       background=[('active', '#28B463')])

        # Gaya khusus untuk tombol Ubah (biru muda, teks putih)
        self.style.configure("Update.Action.TButton",
                             background="#3498DB", 
                             foreground="black")
        self.style.map("Update.Action.TButton",
                       background=[('active', '#2874A6')])

        # Gaya khusus untuk tombol Hapus (merah marun, teks putih)
        self.style.configure("Delete.Action.TButton",
                             background="#E74C3C", 
                             foreground="black")
        self.style.map("Delete.Action.TButton",
                       background=[('active', '#C0392B')])

        # Gaya khusus untuk tombol Bersihkan (abu-abu tua, teks putih)
        self.style.configure("Clear.Action.TButton",
                             background="#7F8C8D",
                             foreground="black")
        self.style.map("Clear.Action.TButton",
                       background=[('active', '#626567')])

        # Gaya khusus untuk tombol Cari dan Tampilkan Semua
        self.style.configure("Search.TButton",
                             font=("Arial", 10, "bold"),
                             padding=6,
                             background="#F39C12", 
                             foreground="black",
                             relief="flat")
        self.style.map("Search.TButton",
                       background=[('active', '#D35400')])

        # Gaya untuk Treeview Header dan Baris
        self.style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#DDDDDD", foreground="#333333")
        self.style.configure("Treeview", rowheight=25, font=("Arial", 9))
        self.style.map('Treeview', background=[('selected', '#AED6F1')]) 
        # --- Akhir Definisi Styles ---

        # Frame untuk Judul
        title_frame = ttk.Frame(self)
        title_frame.pack(pady=10)
        lbl_title = ttk.Label(title_frame, text="📚 Manajemen Data Buku", style="ManagementTitle.TLabel")
        lbl_title.pack()

        # Frame untuk Form Input
        input_frame = ttk.LabelFrame(self, text="📖 Detail Buku", style="Detail.TLabelframe")
        input_frame.pack(pady=10, padx=10, fill="x")

        # Input fields (menggunakan grid di dalam input_frame)
        ttk.Label(input_frame, text="Judul:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_title = ttk.Entry(input_frame, width=40)
        self.entry_title.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(input_frame, text="Pengarang:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_author = ttk.Entry(input_frame, width=40)
        self.entry_author.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(input_frame, text="ISBN:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_isbn = ttk.Entry(input_frame, width=40)
        self.entry_isbn.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(input_frame, text="Kategori:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.entry_category = ttk.Entry(input_frame, width=40)
        self.entry_category.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(input_frame, text="Stok:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_stock = ttk.Entry(input_frame, width=40)
        self.entry_stock.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        input_frame.grid_columnconfigure(1, weight=1)
        input_frame.grid_columnconfigure(3, weight=1)


        # Frame untuk Tombol Aksi
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        # Tombol Aksi dengan Emotikon dan Gaya
        self.btn_add = ttk.Button(button_frame, text="➕ Tambah Buku", command=self.add_book, style="Add.Action.TButton")
        self.btn_add.grid(row=0, column=0, padx=5)

        self.btn_update = ttk.Button(button_frame, text="✏️ Ubah Buku", command=self.update_book, state=tk.DISABLED, style="Update.Action.TButton")
        self.btn_update.grid(row=0, column=1, padx=5)

        self.btn_delete = ttk.Button(button_frame, text="🗑️ Hapus Buku", command=self.delete_book, state=tk.DISABLED, style="Delete.Action.TButton")
        self.btn_delete.grid(row=0, column=2, padx=5)

        self.btn_clear = ttk.Button(button_frame, text="🧹 Bersihkan Form", command=self.clear_form, style="Clear.Action.TButton")
        self.btn_clear.grid(row=0, column=3, padx=5)

        # Frame untuk Pencarian
        search_frame = ttk.LabelFrame(self, text="🔍 Pencarian Buku", style="Detail.TLabelframe") # Emotikon dan style
        search_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(search_frame, text="Cari berdasarkan:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_search = ttk.Entry(search_frame, width=50)
        self.entry_search.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.btn_search = ttk.Button(search_frame, text="🔎 Cari", command=self.search_book, style="Search.TButton") # Emotikon dan style
        self.btn_search.grid(row=0, column=2, padx=5, pady=5)

        self.btn_show_all = ttk.Button(search_frame, text="🔄 Tampilkan Semua", command=self.load_books, style="Search.TButton") # Emotikon dan style
        self.btn_show_all.grid(row=0, column=3, padx=5, pady=5)

        search_frame.grid_columnconfigure(1, weight=1)


        # Frame dan Tabel untuk Menampilkan Data Buku (Treeview)
        table_frame = ttk.Frame(self)
        table_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Scrollbar
        scrollbar_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        scrollbar_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)

        self.tree_books = ttk.Treeview(table_frame, columns=("ID", "Judul", "Pengarang", "ISBN", "Kategori", "Stok", "Tersedia"),
                                       show="headings",
                                       yscrollcommand=scrollbar_y.set,
                                       xscrollcommand=scrollbar_x.set,
                                       style="Treeview") # Terapkan style

        scrollbar_y.config(command=self.tree_books.yview)
        scrollbar_x.config(command=self.tree_books.xview)

        # Define headings
        self.tree_books.heading("ID", text="ID")
        self.tree_books.heading("Judul", text="Judul")
        self.tree_books.heading("Pengarang", text="Pengarang")
        self.tree_books.heading("ISBN", text="ISBN")
        self.tree_books.heading("Kategori", text="Kategori")
        self.tree_books.heading("Stok", text="Stok")
        self.tree_books.heading("Tersedia", text="Tersedia")

        # Define column widths (adjust as needed)
        self.tree_books.column("ID", width=50, anchor="center")
        self.tree_books.column("Judul", width=200)
        self.tree_books.column("Pengarang", width=150)
        self.tree_books.column("ISBN", width=100)
        self.tree_books.column("Kategori", width=100)
        self.tree_books.column("Stok", width=70, anchor="center")
        self.tree_books.column("Tersedia", width=70, anchor="center")

        # Pack the treeview and scrollbars
        self.tree_books.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        # Configure grid weights for table_frame
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Bind selection event (untuk mengisi form saat item di tabel dipilih)
        self.tree_books.bind("<<TreeviewSelect>>", self.on_book_select)

    def load_books(self):
        """Memuat data buku dari database dan menampilkannya di Treeview."""
        for item in self.tree_books.get_children():
            self.tree_books.delete(item)
        try:
            self.db.cursor.execute("SELECT * FROM books ORDER BY title ASC")
            rows = self.db.cursor.fetchall()
            for row in rows:
                self.tree_books.insert("", tk.END, values=row)
            self.entry_search.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error Database", f"Gagal memuat data buku: {e}")

    def add_book(self):
        """Menambahkan buku baru ke database."""
        title = self.entry_title.get()
        author = self.entry_author.get()
        isbn = self.entry_isbn.get()
        category = self.entry_category.get()
        stock_str = self.entry_stock.get()

        if not title or not author or not stock_str:
            messagebox.showwarning("Input Kurang", "Judul, Pengarang, dan Stok harus diisi.")
            return

        try:
            stock = int(stock_str)
            if stock < 0:
                 messagebox.showwarning("Input Tidak Valid", "Stok tidak boleh negatif.")
                 return
        except ValueError:
            messagebox.showwarning("Input Tidak Valid", "Stok harus berupa angka.")
            return

        try:
            if isbn:
                 self.db.cursor.execute("SELECT id FROM books WHERE isbn = ?", (isbn,))
                 if self.db.cursor.fetchone():
                      messagebox.showwarning("ISBN Duplikat", f"Buku dengan ISBN '{isbn}' sudah ada.")
                      return

            self.db.cursor.execute("""
                INSERT INTO books (title, author, isbn, category, stock, available)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (title, author, isbn, category, stock, stock))

            self.db.conn.commit()
            messagebox.showinfo("Sukses", "Buku berhasil ditambahkan.")
            self.clear_form()
            self.load_books()
        except Exception as e:
            messagebox.showerror("Error Database", f"Gagal menambahkan buku: {e}")
            self.db.conn.rollback()

    def update_book(self):
        """Mengubah data buku yang dipilih."""
        selected_item = self.tree_books.focus()
        if not selected_item:
            messagebox.showwarning("Pilih Data", "Pilih buku dari tabel yang ingin diubah.")
            return

        book_id = self.tree_books.item(selected_item, 'values')[0]

        title = self.entry_title.get()
        author = self.entry_author.get()
        isbn = self.entry_isbn.get()
        category = self.entry_category.get()
        stock_str = self.entry_stock.get()

        if not title or not author or not stock_str:
            messagebox.showwarning("Input Kurang", "Judul, Pengarang, dan Stok harus diisi.")
            return

        try:
            stock = int(stock_str)
            if stock < 0:
                 messagebox.showwarning("Input Tidak Valid", "Stok tidak boleh negatif.")
                 return
        except ValueError:
            messagebox.showwarning("Input Tidak Valid", "Stok harus berupa angka.")
            return

        try:
            if isbn:
                 self.db.cursor.execute("SELECT id FROM books WHERE isbn = ? AND id != ?", (isbn, book_id))
                 if self.db.cursor.fetchone():
                      messagebox.showwarning("ISBN Duplikat", f"Buku dengan ISBN '{isbn}' sudah ada pada buku lain.")
                      return

            self.db.cursor.execute("SELECT stock, available FROM books WHERE id = ?", (book_id,))
            old_stock, old_available = self.db.cursor.fetchone()

            stock_change = stock - old_stock
            new_available = old_available + stock_change
            if new_available < 0:
                 messagebox.showwarning("Stok Tidak Cukup", "Jumlah buku tersedia tidak bisa kurang dari 0. Pastikan stok baru mencukupi jumlah buku yang sedang dipinjam.")
                 return

            self.db.cursor.execute("""
                UPDATE books
                SET title = ?, author = ?, isbn = ?, category = ?, stock = ?, available = ?
                WHERE id = ?
            """, (title, author, isbn, category, stock, new_available, book_id))

            self.db.conn.commit()
            messagebox.showinfo("Sukses", "Data buku berhasil diubah.")
            self.clear_form()
            self.load_books()
            self.btn_add.config(state=tk.NORMAL)
            self.btn_update.config(state=tk.DISABLED)
            self.btn_delete.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Error Database", f"Gagal mengubah data buku: {e}")
            self.db.conn.rollback()

    def delete_book(self):
        """Menghapus buku yang dipilih dari database."""
        selected_item = self.tree_books.focus()
        if not selected_item:
            messagebox.showwarning("Pilih Data", "Pilih buku dari tabel yang ingin dihapus.")
            return

        book_id = self.tree_books.item(selected_item, 'values')[0]
        book_title = self.tree_books.item(selected_item, 'values')[1]

        if messagebox.askyesno("Konfirmasi Hapus", f"Yakin ingin menghapus buku '{book_title}'?"):
            try:
                self.db.cursor.execute("SELECT COUNT(*) FROM borrowings WHERE book_id = ? AND status = 'Borrowed'", (book_id,))
                borrow_count = self.db.cursor.fetchone()[0]

                if borrow_count > 0:
                     messagebox.showwarning("Tidak Bisa Dihapus", f"Buku '{book_title}' sedang dipinjam ({borrow_count} eksemplar). Tidak bisa dihapus.")
                     return

                self.db.cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
                self.db.conn.commit()
                messagebox.showinfo("Sukses", "Buku berhasil dihapus.")
                self.clear_form()
                self.load_books()
                self.btn_add.config(state=tk.NORMAL)
                self.btn_update.config(state=tk.DISABLED)
                self.btn_delete.config(state=tk.DISABLED)

            except Exception as e:
                messagebox.showerror("Error Database", f"Gagal menghapus buku: {e}")
                self.db.conn.rollback()

    def clear_form(self):
        """Membersihkan isi form input."""
        self.entry_title.delete(0, tk.END)
        self.entry_author.delete(0, tk.END)
        self.entry_isbn.delete(0, tk.END)
        self.entry_category.delete(0, tk.END)
        self.entry_stock.delete(0, tk.END)
        if self.tree_books.focus():
            self.tree_books.selection_remove(self.tree_books.focus())
        self.btn_add.config(state=tk.NORMAL)
        self.btn_update.config(state=tk.DISABLED)
        self.btn_delete.config(state=tk.DISABLED)

    def on_book_select(self, event):
        """Mengisi form input saat item di treeview dipilih."""
        selected_item = self.tree_books.focus()
        if selected_item:
            values = self.tree_books.item(selected_item, 'values')
            self.clear_form()
            self.entry_title.insert(0, values[1])
            self.entry_author.insert(0, values[2])
            self.entry_isbn.insert(0, values[3])
            self.entry_category.insert(0, values[4])
            self.entry_stock.insert(0, values[5])

            self.btn_add.config(state=tk.DISABLED)
            self.btn_update.config(state=tk.NORMAL)
            self.btn_delete.config(state=tk.NORMAL)
        else:
             self.clear_form()

    def search_book(self):
        """Mencari buku berdasarkan kriteria."""
        search_term = self.entry_search.get()
        if not search_term:
            self.load_books()
            return
        try:
            for item in self.tree_books.get_children():
                self.tree_books.delete(item)
            query = """
                SELECT * FROM books
                WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ? OR category LIKE ?
                ORDER BY title ASC
            """
            search_like = f"%{search_term}%"
            self.db.cursor.execute(query, (search_like, search_like, search_like, search_like))
            rows = self.db.cursor.fetchall()
            if rows:
                for row in rows:
                    self.tree_books.insert("", tk.END, values=row)
            else:
                messagebox.showinfo("Pencarian", f"Tidak ada buku yang cocok dengan '{search_term}'.")
        except Exception as e:
            messagebox.showerror("Error Database", f"Gagal mencari buku: {e}")

    def on_show(self):
        """Dipanggil saat frame ini ditampilkan."""
        print("Book Management frame shown. Loading books...")
        self.load_books()
        self.clear_form()