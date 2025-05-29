import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from database import Database
from login_frame import LoginFrame
from dashboard_frame import DashboardFrame
from book_management import BookManagementFrame
from member_management import MemberManagementFrame
from borrowing_management import BorrowingManagementFrame
from report_frame import ReportFrame
from profile_settings_frame import ProfileSettingsFrame
from about_frame import AboutFrame
from help_frame import HelpFrame
from member_dashboard_frame import MemberDashboardFrame

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Manajemen Perpustakaan")

        self.db = Database()

        # --- TEMA GLOBAL ---
        self.root.set_theme("arc") 
        self.style = ttk.Style(self.root)

        self.current_user_id = None
        self.current_user_role = None
        self.current_username = None
        self.current_member_id = None

        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        self.create_menu()

        self.container = ttk.Frame(root)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        login_frame = LoginFrame(self.container, self, self.style)
        login_frame.grid(row=0, column=0, sticky="nsew")
        self.frames["Login"] = login_frame

        dashboard_frame = DashboardFrame(self.container, self, self.style)
        dashboard_frame.grid(row=0, column=0, sticky="nsew")
        self.frames["Dashboard"] = dashboard_frame

        book_management_frame = BookManagementFrame(self.container, self, self.style)
        book_management_frame.grid(row=0, column=0, sticky="nsew")
        self.frames["ManajemenBuku"] = book_management_frame

        member_management_frame = MemberManagementFrame(self.container, self, self.style)
        member_management_frame.grid(row=0, column=0, sticky="nsew")
        self.frames["ManajemenAnggota"] = member_management_frame

        borrowing_management_frame = BorrowingManagementFrame(self.container, self, self.style)
        borrowing_management_frame.grid(row=0, column=0, sticky="nsew")
        self.frames["ManajemenPeminjaman"] = borrowing_management_frame

        report_frame = ReportFrame(self.container, self, self.style)
        report_frame.grid(row=0, column=0, sticky="nsew")
        self.frames["Laporan"] = report_frame

        profile_settings_frame = ProfileSettingsFrame(self.container, self, self.style)
        profile_settings_frame.grid(row=0, column=0, sticky="nsew")
        self.frames["PengaturanProfil"] = profile_settings_frame

        about_frame = AboutFrame(self.container, self, self.style)
        about_frame.grid(row=0, column=0, sticky="nsew")
        self.frames["TentangAplikasi"] = about_frame

        help_frame = HelpFrame(self.container, self, self.style)
        help_frame.grid(row=0, column=0, sticky="nsew")
        self.frames["Bantuan"] = help_frame

        member_dashboard_frame = MemberDashboardFrame(self.container, self, self.style)
        member_dashboard_frame.grid(row=0, column=0, sticky="nsew")
        self.frames["MemberDashboard"] = member_dashboard_frame

        # Inisialisasi status fullscreen
        self.is_fullscreen = True

        self.show_frame("Login")
        
        # Binding event Esc untuk keluar dari fullscreen
        self.root.bind("<Escape>", self.toggle_fullscreen)

    def create_menu(self):
        self.account_menu = tk.Menu(self.menubar, tearoff=0)
        self.management_menu = tk.Menu(self.menubar, tearoff=0)

        help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Bantuan", menu=help_menu)
        help_menu.add_command(label="Panduan Penggunaan", command=lambda: self.show_frame("Bantuan"))
        help_menu.add_separator()
        help_menu.add_command(label="Tentang Aplikasi", command=lambda: self.show_frame("TentangAplikasi"))

        # Tambahkan menu untuk keluar dari fullscreen atau menutup aplikasi jika diperlukan
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Jendela", menu=file_menu)
        file_menu.add_command(label="Keluar Fullscreen (Esc)", command=lambda: self.toggle_fullscreen(None))
        file_menu.add_separator()
        file_menu.add_command(label="Keluar Aplikasi", command=self.root.quit)


    def update_menus(self):
        for label in ["Akun", "Manajemen"]:
            try: self.menubar.delete(label)
            except tk.TclError: pass

        if self.current_username:
            self.account_menu.delete(0, tk.END)
            self.account_menu.add_command(label="Pengaturan Profil", command=lambda: self.show_frame("PengaturanProfil"))
            self.account_menu.add_separator()
            self.account_menu.add_command(label="Logout", command=self.logout)
            self.menubar.insert_cascade(0, label="Akun", menu=self.account_menu)

            if self.current_user_role in ["admin", "petugas"]:
                self.management_menu.delete(0, tk.END)
                self.management_menu.add_command(label="Dashboard Admin", command=lambda: self.show_frame("Dashboard"))
                self.management_menu.add_command(label="Manajemen Buku", command=lambda: self.show_frame("ManajemenBuku"))
                self.management_menu.add_command(label="Manajemen Anggota", command=lambda: self.show_frame("ManajemenAnggota"))
                self.management_menu.add_command(label="Peminjaman & Pengembalian", command=lambda: self.show_frame("ManajemenPeminjaman"))
                self.management_menu.add_command(label="Laporan", command=lambda: self.show_frame("Laporan"))
                self.menubar.insert_cascade(1, label="Manajemen", menu=self.management_menu)
            elif self.current_user_role == "member":
                pass

    # Fungsi baru untuk mengaktifkan/menonaktifkan mode fullscreen
    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)
        if not self.is_fullscreen: 
            self.root.geometry("1000x700") 
            self.root.resizable(True, True) 
        self.update_menus()


    def show_frame(self, page_name):
        frame = self.frames[page_name]

        # Selalu coba masuk mode fullscreen ketika berpindah frame, jika belum fullscreen
        if not self.is_fullscreen:
            self.root.attributes("-fullscreen", True)
            self.is_fullscreen = True

        self.update_menus() 
        frame.tkraise()
        if hasattr(frame, 'on_show'):
            frame.on_show()

    def show_main_app(self, username, role, member_id):
        user_data = self.db.get_user(username)
        if user_data:
            user_id, _, _, _, _ = user_data
            self.current_user_id = user_id
        else:
            self.current_user_id = None

        self.current_username = username
        self.current_user_role = role
        self.current_member_id = member_id

        print(f"Login berhasil. User ID: {self.current_user_id}, User: {self.current_username}, Role: {self.current_user_role}, Member ID: {self.current_member_id}")

        self.update_menus()

        if self.current_user_role in ["admin", "petugas"]:
            self.show_frame("Dashboard") 
        elif self.current_user_role == "member":
            self.show_frame("MemberDashboard") 

    def logout(self):
        self.current_user_id = None
        self.current_user_role = None
        self.current_username = None
        self.current_member_id = None
        self.update_menus()
        # Saat logout, kita tetap ingin di mode fullscreen
        self.show_frame("Login")
        print("User logged out.")

if __name__ == "__main__":
    root = ThemedTk()
    app = LibraryApp(root)
    root.mainloop()