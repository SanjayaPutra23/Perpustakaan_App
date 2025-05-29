import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class MemberManagementFrame(ttk.Frame):
    # --- UBAH BARIS INI: Terima 'style_instance' ---
    def __init__(self, parent, controller, style_instance):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = self.controller.db

        self.style = style_instance

        # --- Definisi Styles ---
        self.style.configure("ManagementTitle.TLabel", font=("Arial", 18, "bold"), foreground="#007BFF") 
        # Gaya untuk LabelFrame (box detail anggota)
        self.style.configure("Detail.TLabelframe.Label", font=("Arial", 11, "bold"), foreground="#333333") 
        self.style.configure("Detail.TLabelframe", background="#F0F0F0", relief="solid", borderwidth=1) 

        # Gaya untuk Tombol Aksi (Tambah, Ubah, Hapus, Bersihkan)
        self.style.configure("Action.TButton",
                             font=("Arial", 10, "bold"),
                             padding=8,
                             relief="flat") 

        # Gaya khusus untuk tombol Tambah (Biru Langit)
        self.style.configure("Add.Action.TButton",
                             background="#87CEEB", 
                             foreground="black") 
        self.style.map("Add.Action.TButton",
                       background=[('active', '#6A9BC0')]) 

        # Gaya khusus untuk tombol Ubah (Oranye)
        self.style.configure("Update.Action.TButton",
                             background="#FFA500",
                             foreground="black") 
        self.style.map("Update.Action.TButton",
                       background=[('active', '#CC8400')]) 

        # Gaya khusus untuk tombol Hapus (Merah)
        self.style.configure("Delete.Action.TButton",
                             background="#DC3545", 
                             foreground="black") 
        self.style.map("Delete.Action.TButton",
                       background=[('active', '#C82333')]) 

        # Gaya khusus untuk tombol Bersihkan (Abu-abu)
        self.style.configure("Clear.Action.TButton",
                             background="#6C757D",
                             foreground="black") 
        self.style.map("Clear.Action.TButton",
                       background=[('active', '#5A6268')])

        # Gaya untuk Treeview Header dan Baris
        self.style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#DDDDDD", foreground="#333333")
        self.style.configure("Treeview", rowheight=25, font=("Arial", 9))
        self.style.map('Treeview', background=[('selected', '#B0C4DE')]) 

        # Frame untuk Judul
        title_frame = ttk.Frame(self)
        title_frame.pack(pady=10)
        lbl_title = ttk.Label(title_frame, text="👥 Manajemen Data Anggota", style="ManagementTitle.TLabel")
        lbl_title.pack()

        # Frame untuk Form Input
        input_frame = ttk.LabelFrame(self, text="📝 Detail Anggota", style="Detail.TLabelframe")
        input_frame.pack(pady=10, padx=10, fill="x")

        # Input fields (menggunakan grid di dalam input_frame)
        ttk.Label(input_frame, text="Nama:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_name = ttk.Entry(input_frame, width=40)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(input_frame, text="Alamat:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_address = ttk.Entry(input_frame, width=40)
        self.entry_address.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(input_frame, text="Telepon:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_phone = ttk.Entry(input_frame, width=40)
        self.entry_phone.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(input_frame, text="Email:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.entry_email = ttk.Entry(input_frame, width=40)
        self.entry_email.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        # Konfigurasi kolom agar entry fields bisa melebar
        input_frame.grid_columnconfigure(1, weight=1)
        input_frame.grid_columnconfigure(3, weight=1)

        # Frame untuk Tombol Aksi
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        # --- Tombol Aksi dengan Emotikon Unicode ---
        self.btn_add = ttk.Button(button_frame, text="➕ Tambah Anggota", command=self.add_member, style="Add.Action.TButton")
        self.btn_add.grid(row=0, column=0, padx=5)

        self.btn_update = ttk.Button(button_frame, text="✏️ Ubah Anggota", command=self.update_member, state=tk.DISABLED, style="Update.Action.TButton")
        self.btn_update.grid(row=0, column=1, padx=5)

        self.btn_delete = ttk.Button(button_frame, text="🗑️ Hapus Anggota", command=self.delete_member, state=tk.DISABLED, style="Delete.Action.TButton")
        self.btn_delete.grid(row=0, column=2, padx=5)

        self.btn_clear = ttk.Button(button_frame, text="🧹 Bersihkan Form", command=self.clear_form, style="Clear.Action.TButton")
        self.btn_clear.grid(row=0, column=3, padx=5)

        # Frame dan Tabel untuk Menampilkan Data Anggota (Treeview)
        table_frame = ttk.Frame(self)
        table_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Scrollbar
        scrollbar_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        scrollbar_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)

        self.tree_members = ttk.Treeview(table_frame, columns=("ID", "Nama", "Alamat", "Telepon", "Email"),
                                         show="headings",
                                         yscrollcommand=scrollbar_y.set,
                                         xscrollcommand=scrollbar_x.set,
                                         style="Treeview") 
        scrollbar_y.config(command=self.tree_members.yview)
        scrollbar_x.config(command=self.tree_members.xview)

        # Define headings
        self.tree_members.heading("ID", text="ID")
        self.tree_members.heading("Nama", text="Nama")
        self.tree_members.heading("Alamat", text="Alamat")
        self.tree_members.heading("Telepon", text="Telepon")
        self.tree_members.heading("Email", text="Email")

        # Define column widths (adjust as needed)
        self.tree_members.column("ID", width=50, anchor="center")
        self.tree_members.column("Nama", width=150)
        self.tree_members.column("Alamat", width=200)
        self.tree_members.column("Telepon", width=100)
        self.tree_members.column("Email", width=150)

        # Pack the treeview and scrollbars
        self.tree_members.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        # Configure grid weights for table_frame
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Bind selection event (untuk mengisi form saat item di tabel dipilih)
        self.tree_members.bind("<<TreeviewSelect>>", self.on_member_select)

    def load_members(self):
        """Memuat data anggota dari database dan menampilkannya di Treeview."""
        for item in self.tree_members.get_children():
            self.tree_members.delete(item)
        try:
            self.db.cursor.execute("SELECT * FROM members")
            rows = self.db.cursor.fetchall()
            for row in rows:
                self.tree_members.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error Database", f"Gagal memuat data anggota: {e}")

    def add_member(self):
        """Menambahkan anggota baru ke database."""
        name = self.entry_name.get()
        address = self.entry_address.get()
        phone = self.entry_phone.get()
        email = self.entry_email.get()

        if not name:
            messagebox.showwarning("Input Kurang", "Nama anggota harus diisi.")
            return

        try:
            if phone:
                self.db.cursor.execute("SELECT id FROM members WHERE phone = ?", (phone,))
                if self.db.cursor.fetchone():
                    messagebox.showwarning("Duplikat", f"Nomor telepon '{phone}' sudah terdaftar.")
                    return
            if email:
                self.db.cursor.execute("SELECT id FROM members WHERE email = ?", (email,))
                if self.db.cursor.fetchone():
                    messagebox.showwarning("Duplikat", f"Email '{email}' sudah terdaftar.")
                    return

            self.db.cursor.execute("""
                INSERT INTO members (name, address, phone, email)
                VALUES (?, ?, ?, ?)
            """, (name, address, phone, email))
            self.db.conn.commit()
            messagebox.showinfo("Sukses", "Anggota berhasil ditambahkan.")
            self.clear_form()
            self.load_members()
        except Exception as e:
            messagebox.showerror("Error Database", f"Gagal menambahkan anggota: {e}")
            self.db.conn.rollback()

    def update_member(self):
        """Mengubah data anggota yang dipilih."""
        selected_item = self.tree_members.focus()
        if not selected_item:
            messagebox.showwarning("Pilih Data", "Pilih anggota dari tabel yang ingin diubah.")
            return

        member_id = self.tree_members.item(selected_item, 'values')[0]

        name = self.entry_name.get()
        address = self.entry_address.get()
        phone = self.entry_phone.get()
        email = self.entry_email.get()

        if not name:
            messagebox.showwarning("Input Kurang", "Nama anggota harus diisi.")
            return

        try:
            if phone:
                self.db.cursor.execute("SELECT id FROM members WHERE phone = ? AND id != ?", (phone, member_id))
                if self.db.cursor.fetchone():
                    messagebox.showwarning("Duplikat", f"Nomor telepon '{phone}' sudah terdaftar pada anggota lain.")
                    return
            if email:
                self.db.cursor.execute("SELECT id FROM members WHERE email = ? AND id != ?", (email, member_id))
                if self.db.cursor.fetchone():
                    messagebox.showwarning("Duplikat", f"Email '{email}' sudah terdaftar pada anggota lain.")
                    return

            self.db.cursor.execute("""
                UPDATE members
                SET name = ?, address = ?, phone = ?, email = ?
                WHERE id = ?
            """, (name, address, phone, email, member_id))

            self.db.conn.commit()
            messagebox.showinfo("Sukses", "Data anggota berhasil diubah.")
            self.clear_form()
            self.load_members()
            self.btn_add.config(state=tk.NORMAL)
            self.btn_update.config(state=tk.DISABLED)
            self.btn_delete.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Error Database", f"Gagal mengubah data anggota: {e}")
            self.db.conn.rollback()

    def delete_member(self):
        """Menghapus anggota yang dipilih dari database."""
        selected_item = self.tree_members.focus()
        if not selected_item:
            messagebox.showwarning("Pilih Data", "Pilih anggota dari tabel yang ingin dihapus.")
            return

        member_id = self.tree_members.item(selected_item, 'values')[0]
        member_name = self.tree_members.item(selected_item, 'values')[1]

        if messagebox.askyesno("Konfirmasi Hapus", f"Yakin ingin menghapus anggota '{member_name}'?"):
            try:
                self.db.cursor.execute("SELECT COUNT(*) FROM borrowings WHERE member_id = ? AND status = 'Borrowed'", (member_id,))
                borrow_count = self.db.cursor.fetchone()[0]

                if borrow_count > 0:
                    messagebox.showwarning("Tidak Bisa Dihapus", f"Anggota '{member_name}' masih memiliki {borrow_count} pinjaman aktif. Tidak bisa dihapus.")
                    return

                self.db.cursor.execute("DELETE FROM members WHERE id = ?", (member_id,))
                self.db.conn.commit()
                messagebox.showinfo("Sukses", "Anggota berhasil dihapus.")
                self.clear_form()
                self.load_members()
                self.btn_add.config(state=tk.NORMAL)
                self.btn_update.config(state=tk.DISABLED)
                self.btn_delete.config(state=tk.DISABLED)

            except Exception as e:
                messagebox.showerror("Error Database", f"Gagal menghapus anggota: {e}")
                self.db.conn.rollback()

    def clear_form(self):
        """Membersihkan isi form input."""
        self.entry_name.delete(0, tk.END)
        self.entry_address.delete(0, tk.END)
        self.entry_phone.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.tree_members.selection_remove(self.tree_members.focus())
        self.btn_add.config(state=tk.NORMAL)
        self.btn_update.config(state=tk.DISABLED)
        self.btn_delete.config(state=tk.DISABLED)

    def on_member_select(self, event):
        """Mengisi form input saat item di treeview dipilih."""
        selected_item = self.tree_members.focus()
        if selected_item:
            values = self.tree_members.item(selected_item, 'values')
            self.clear_form()
            self.entry_name.insert(0, values[1])
            self.entry_address.insert(0, values[2])
            self.entry_phone.insert(0, values[3])
            self.entry_email.insert(0, values[4])

            self.btn_add.config(state=tk.DISABLED)
            self.btn_update.config(state=tk.NORMAL)
            self.btn_delete.config(state=tk.NORMAL)
        else:
            self.clear_form()

    def on_show(self):
        """Dipanggil saat frame ini ditampilkan."""
        print("Member Management frame shown. Loading members...")
        self.load_members()
        self.clear_form()