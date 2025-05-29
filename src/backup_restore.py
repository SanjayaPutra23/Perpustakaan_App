import shutil
import os
from tkinter import filedialog, messagebox
from datetime import datetime

def backup_database(original_db_path="perpustakaan.db"):
    """
    Membuat backup dari file database SQLite.

    Args:
        original_db_path (str): Path ke file database yang ingin di-backup.
    """
    if not os.path.exists(original_db_path):
        messagebox.showerror("Error Backup", f"File database sumber tidak ditemukan: {original_db_path}")
        return

    try:
        # Generate nama file backup default dengan timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_backup_filename = f"library_backup_{timestamp}.db"

        backup_file_path = filedialog.asksaveasfilename(
            defaultextension=".db",
            filetypes=[("SQLite Database Files", "*.db"), ("All Files", "*.*")],
            title="Simpan Backup Database Sebagai...",
            initialfile=default_backup_filename
        )

        if not backup_file_path:
            messagebox.showinfo("Backup Dibatalkan", "Operasi backup database dibatalkan.")
            return

        shutil.copy2(original_db_path, backup_file_path)
        messagebox.showinfo("Backup Berhasil", f"Database berhasil di-backup ke:\n{backup_file_path}")

    except Exception as e:
        messagebox.showerror("Error Backup", f"Gagal melakukan backup database: {e}")

def restore_database(target_db_path="perpustakaan.db"):
    """
    Me-restore database dari file backup.

    Args:
        target_db_path (str): Path ke file database yang ingin di-restore (akan ditimpa).
    """
    try:
        backup_file_path = filedialog.askopenfilename(
            defaultextension=".db",
            filetypes=[("SQLite Database Files", "*.db"), ("All Files", "*.*")],
            title="Pilih File Backup Database untuk Restore"
        )

        if not backup_file_path:
            messagebox.showinfo("Restore Dibatalkan", "Operasi restore database dibatalkan.")
            return

        if not os.path.exists(backup_file_path):
            messagebox.showerror("Error Restore", f"File backup tidak ditemukan: {backup_file_path}")
            return

        # Konfirmasi penting sebelum menimpa database
        confirm = messagebox.askyesno(
            "Konfirmasi Restore",
            f"PERINGATAN: Ini akan menimpa database saat ini ({target_db_path}) dengan konten dari:\n{backup_file_path}\n\n"
            "Semua data saat ini yang belum di-backup akan hilang.\n"
            "Lanjutkan?"
        )

        if not confirm:
            messagebox.showinfo("Restore Dibatalkan", "Operasi restore database dibatalkan oleh pengguna.")
            return

        shutil.copy2(backup_file_path, target_db_path)
        messagebox.showinfo("Restore Berhasil",
                            f"Database berhasil di-restore dari:\n{backup_file_path}\n\n"
                            "Disarankan untuk me-restart aplikasi agar perubahan diterapkan sepenuhnya.")

    except Exception as e:
        messagebox.showerror("Error Restore", f"Gagal melakukan restore database: {e}")

if __name__ == '__main__':
    # root.mainloop()
    print("Fungsi backup_database dan restore_database siap digunakan.")
    print("Jalankan dari aplikasi utama untuk fungsionalitas penuh.")

