import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os 

class LoginFrame(ttk.Frame):
    def __init__(self, parent, controller, style_instance):
        super().__init__(parent)
        self.controller = controller
        self.db = self.controller.db
        
        self.style = style_instance 
        
        # --- DEFINISI STYLES KUSTOM DI SINI ---
        self.style.configure("LoginTitle.TLabel", 
                             font=("Arial", 22, "bold"), 
                             foreground="#4A90E2")
        
        self.style.configure("LoginInputLabel.TLabel", 
                             font=("Arial", 12, "bold"))
        
        self.style.configure("LoginEntry.TEntry", 
                             font=("Arial", 12))
        
        self.style.configure("Accent.TButton", 
                             font=("Arial", 11, "bold"), 
                             background="#007BFF", 
                             foreground="black", 
                             padding=10)
        self.style.map("Accent.TButton",
                       background=[('active', '#0056b3')],
                       foreground=[('disabled', '#AAAAAA')])
        
        # Style khusus untuk Checkbutton "Tampilkan Password"
        self.style.configure("ShowPassword.TCheckbutton",
                             font=("Arial", 9))

        self.create_widgets()
        self.check_admin_exists() 

    def create_widgets(self):
        login_container = ttk.Frame(self)
        login_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        lbl_title = ttk.Label(login_container, text="Aplikasi Perpustakaan 📚", 
                              style="LoginTitle.TLabel")
        lbl_title.grid(row=0, column=0, columnspan=2, pady=(30, 20), padx=20)

        # --- Input Username ---
        ttk.Label(login_container, text="👤 Username:", 
                  style="LoginInputLabel.TLabel").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_username = ttk.Entry(login_container, width=35,
                                        style="LoginEntry.TEntry")
        self.entry_username.grid(row=1, column=1, padx=10, pady=10)
        self.entry_username.focus()

        # --- Input Password ---
        ttk.Label(login_container, text="🔒 Password:", 
                  style="LoginInputLabel.TLabel").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        
        # Frame untuk menampung Entry Password dan Checkbutton
        password_input_frame = ttk.Frame(login_container)
        password_input_frame.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.entry_password = ttk.Entry(password_input_frame, show="*", width=35,
                                        style="LoginEntry.TEntry")
        self.entry_password.pack(side="left", fill="x", expand=True)
        
        # Variabel untuk melacak status password (tersembunyi/terlihat)
        self.show_password_var = tk.BooleanVar(value=False)

        # Checkbutton untuk toggle password visibility
        self.toggle_password_checkbutton = ttk.Checkbutton(
            login_container,
            text="Tampilkan Password",
            command=self.toggle_password_visibility,
            variable=self.show_password_var,
            style="ShowPassword.TCheckbutton"
        )
        # Posisikan di bawah password entry, di bawah kolom kedua
        self.toggle_password_checkbutton.grid(row=2, column=1, pady=(60, 0), padx=10, sticky="w")


        # --- Tombol Login yang Stylish ---
        btn_login = ttk.Button(login_container, text="Masuk ▶️", 
                               command=self.attempt_login, 
                               width=20, 
                               style="Accent.TButton")
        btn_login.grid(row=3, column=0, columnspan=2, pady=(20, 30))

        # --- Binding Enter Key ---
        self.entry_username.bind("<Return>", lambda event: self.entry_password.focus())
        self.entry_password.bind("<Return>", self.attempt_login)

    # --- Fungsi untuk mengubah visibilitas password ---
    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.entry_password.config(show="")
        else: # Jika Checkbutton tidak dicentang (False)
            self.entry_password.config(show="*")

    def check_admin_exists(self):
        if not os.path.exists("perpustakaan.db") or not self.db.get_user("admin"):
            print("Creating default admin...")
            self.db.create_default_admin()
            print("Default admin created.")

    def attempt_login(self, event=None):
        username = self.entry_username.get()
        password = self.entry_password.get()

        print(f"Login attempt for username: '{username}'")

        if not username or not password:
            messagebox.showwarning("Input Kurang", "Username dan Password harus diisi. ⚠️")
            return

        user_data = self.db.get_user(username)

        if user_data:
            user_id, stored_username, stored_password_hash, role, member_id = user_data
            print(f"User data found: {user_data}")
            if self.db.verify_password(stored_password_hash, password):
                messagebox.showinfo("Login Berhasil", f"Selamat datang, {username}! 🎉")
                self.controller.show_main_app(username, role, member_id)
            else:
                print("Password verification failed.")
                messagebox.showerror("Login Gagal", "Password salah. 🚫")
        else:
            print(f"User '{username}' not found in database.")
            messagebox.showerror("Login Gagal", "Username tidak ditemukan. ❌")

        # Selalu kosongkan password dan sembunyikan kembali setelah percobaan login
        self.entry_password.delete(0, tk.END)
        self.entry_password.config(show="*")
        self.show_password_var.set(False) # Reset Checkbutton

    def on_show(self):
        # Reset input dan status password saat frame ditampilkan (setelah logout)
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.entry_password.config(show="*") 
        self.show_password_var.set(False)
        self.entry_username.focus()