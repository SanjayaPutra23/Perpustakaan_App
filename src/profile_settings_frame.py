import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class ProfileSettingsFrame(ttk.Frame):
    def __init__(self, parent, controller, style_instance): 
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = self.controller.db

        # Inisialisasi Style
        self.style = style_instance 

        # --- Definisi Styles ---
        # Gaya untuk Judul Frame
        # Warna foreground bisa diatur agar kontras di kedua tema
        self.style.configure("ProfileTitle.TLabel", font=("Arial", 18, "bold"), foreground="#4A90E2") 
        
        # Gaya untuk LabelFrame (box ganti password)
        # Background dan foreground dari LabelFrame.Label akan disesuaikan tema secara otomatis,
        # kecuali Anda override eksplisit di sini.
        self.style.configure("PasswordForm.TLabelframe.Label", font=("Arial", 11, "bold"), foreground="#333333")
        self.style.configure("PasswordForm.TLabelframe", background="#F8F8F8", relief="solid", borderwidth=1)

        # Gaya untuk Label input (Username, Password Saat Ini, dll)
        self.style.configure("InputLabel.TLabel", font=("Arial", 10), foreground="#555555")
        self.style.configure("UsernameDisplay.TLabel", font=("Arial", 10, "bold"), foreground="#007BFF")


        # Gaya untuk Tombol Simpan Password Baru
        self.style.configure("SavePassword.TButton",
                             font=("Arial", 10, "bold"),
                             background="#28A745",
                             foreground="black", 
                             padding="8 15")
        self.style.map("SavePassword.TButton",
                       background=[('active', '#218838'), ('!disabled', '#28A745')],
                       foreground=[('disabled', '#AAAAAA')])

        # Gaya untuk Tombol Kembali ke Dashboard
        self.style.configure("Back.TButton",
                             font=("Arial", 10),
                             background="#6C757D", 
                             foreground="black", 
                             padding="8 10")
        self.style.map("Back.TButton",
                       background=[('active', '#5A6268'), ('!disabled', '#6C757D')],
                       foreground=[('disabled', '#AAAAAA')])


        # Frame untuk Judul
        title_frame = ttk.Frame(self)
        title_frame.pack(pady=20)
        lbl_title = ttk.Label(title_frame, text="⚙️ Pengaturan Profil Pengguna", style="ProfileTitle.TLabel") 
        lbl_title.pack()

        # Frame untuk Form Ganti Password
        form_frame = ttk.LabelFrame(self, text="🔑 Ganti Password", style="PasswordForm.TLabelframe") 
        form_frame.pack(pady=10, padx=20)

        # Username (ditampilkan, tidak bisa diubah)
        ttk.Label(form_frame, text="Username:", style="InputLabel.TLabel").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.lbl_username = ttk.Label(form_frame, text="-", style="UsernameDisplay.TLabel") 
        self.lbl_username.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Password Saat Ini
        ttk.Label(form_frame, text="Password Saat Ini:", style="InputLabel.TLabel").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_current_password = ttk.Entry(form_frame, show="*", width=30)
        self.entry_current_password.grid(row=1, column=1, padx=10, pady=5)

        # Password Baru
        ttk.Label(form_frame, text="Password Baru:", style="InputLabel.TLabel").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_new_password = ttk.Entry(form_frame, show="*", width=30)
        self.entry_new_password.grid(row=2, column=1, padx=10, pady=5)

        # Konfirmasi Password Baru
        ttk.Label(form_frame, text="Konfirmasi Password Baru:", style="InputLabel.TLabel").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.entry_confirm_password = ttk.Entry(form_frame, show="*", width=30)
        self.entry_confirm_password.grid(row=3, column=1, padx=10, pady=5)

        # Tombol Simpan Perubahan
        btn_save_password = ttk.Button(form_frame, text="💾 Simpan Password Baru", command=self.change_password, style="SavePassword.TButton")
        btn_save_password.grid(row=4, column=0, columnspan=2, pady=15)

        # Tombol Kembali ke Dashboard
        btn_back = ttk.Button(self, text="⬅️ Kembali ke Dashboard", command=self.back_to_appropriate_dashboard, style="Back.TButton") 
        btn_back.pack(pady=20)

    def change_password(self):
        """Mengubah password pengguna yang sedang login."""
        current_password = self.entry_current_password.get()
        new_password = self.entry_new_password.get()
        confirm_password = self.entry_confirm_password.get()

        if not current_password or not new_password or not confirm_password:
            messagebox.showwarning("Input Kurang", "Semua field password harus diisi.")
            return

        if new_password != confirm_password:
            messagebox.showerror("Password Tidak Cocok", "Password baru dan konfirmasi password tidak cocok.")
            self.entry_new_password.delete(0, tk.END)
            self.entry_confirm_password.delete(0, tk.END)
            return

        if len(new_password) < 6:
            messagebox.showwarning("Password Lemah", "Password baru minimal harus 6 karakter.")
            return

        current_username = getattr(self.controller, 'current_username', None)
        if not current_username:
            messagebox.showerror("Error", "Tidak dapat mengidentifikasi pengguna yang login.")
            return

        user_data = self.db.get_user(current_username)
        if not user_data:
            messagebox.showerror("Error", f"Data pengguna '{current_username}' tidak ditemukan.")
            return

        user_id, stored_username, stored_password_hash, role, member_id = user_data

        if not self.db.verify_password(stored_password_hash, current_password):
            messagebox.showerror("Gagal", "Password saat ini salah.")
            self.entry_current_password.delete(0, tk.END)
            return

        try:
            new_password_hash = self.db.hash_password(new_password)
            self.db.cursor.execute("UPDATE users SET password_hash = ? WHERE username = ?",
                                   (new_password_hash, current_username))
            self.db.conn.commit()
            messagebox.showinfo("Sukses", "Password berhasil diubah. 🎉")
            self.clear_form()
        except Exception as e:
            self.db.conn.rollback()
            messagebox.showerror("Error Database", f"Gagal mengubah password: {e}")

    def clear_form(self):
        """Membersihkan semua field input password."""
        self.entry_current_password.delete(0, tk.END)
        self.entry_new_password.delete(0, tk.END)
        self.entry_confirm_password.delete(0, tk.END)

    def on_show(self):
        """Dipanggil saat frame ini ditampilkan."""
        self.clear_form()
        current_username = getattr(self.controller, 'current_username', "Tidak Diketahui")
        self.lbl_username.config(text=current_username)
        self.entry_current_password.focus()

    def back_to_appropriate_dashboard(self):
        """
        Mengarahkan pengguna kembali ke dashboard yang sesuai
        berdasarkan peran (role) yang sedang login.
        """
        user_role = self.controller.current_user_role

        if user_role == "member":
            self.controller.show_frame("MemberDashboard")
        elif user_role in ["admin", "petugas"]:
            self.controller.show_frame("Dashboard")
        else:
            messagebox.showwarning("Navigasi", "Role pengguna tidak dikenal. Kembali ke halaman login.")
            self.controller.logout()