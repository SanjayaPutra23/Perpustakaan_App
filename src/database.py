# File: library_app/database.py
import sqlite3
import hashlib
from datetime import datetime, timedelta

# Konstanta untuk tarif denda per hari (misalnya, Rp 500)
FINE_PER_DAY = 50000

class Database:
    def __init__(self, db_file="perpustakaan.db"):
        self.db_file = db_file
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
        self.create_default_admin() 
        self.create_default_members_and_users()
        self.create_default_books() 
        

    def connect(self):
        """Connect to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.cursor = self.conn.cursor()
            print(f"Connected to database: {self.db_file}")
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")

    def disconnect(self):
        """Disconnect from the database."""
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

    def hash_password(self, password):
        """Hash a password for storing."""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def verify_password(self, stored_password_hash, provided_password):
        """Verify a stored password against one provided by user"""
        return stored_password_hash == self.hash_password(provided_password) 

    def create_tables(self):
        """Create necessary tables if they don't exist."""
        try:
            # Table for Books
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    isbn TEXT UNIQUE,
                    category TEXT,
                    stock INTEGER DEFAULT 0,
                    available INTEGER DEFAULT 0
                )
            """)

            # Table for Members
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    address TEXT,
                    phone TEXT UNIQUE,
                    email TEXT UNIQUE
                )
            """)

            # Table for Borrowings
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS borrowings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER,
                    member_id INTEGER,
                    borrow_date TEXT NOT NULL,
                    return_date TEXT,
                    status TEXT NOT NULL, -- e.g., 'Borrowed', 'Returned', 'Overdue'
                    fine_amount REAL DEFAULT 0.0, -- Kolom baru untuk denda
                    FOREIGN KEY (book_id) REFERENCES books(id),
                    FOREIGN KEY (member_id) REFERENCES members(id)
                )
            """)

            # Table for Users (Admin/Petugas/Member)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL, -- e.g., 'admin', 'petugas', 'member'
                    member_id INTEGER UNIQUE, -- Link ke tabel members (NULL untuk admin/petugas)
                    FOREIGN KEY (member_id) REFERENCES members(id)
                )
            """)

            self.conn.commit()
            print("Tables checked/created successfully.")

        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    # --- Metode baru untuk membuat admin default ---
    def create_default_admin(self):
        """Add default admin user if users table has no admin."""
        try:
            self.cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
            admin_count = self.cursor.fetchone()[0]
            if admin_count == 0:
                default_username = "admin"
                default_password = "admin123"
                hashed_password = self.hash_password(default_password)
                self.cursor.execute("""
                    INSERT INTO users (username, password_hash, role, member_id)
                    VALUES (?, ?, ?, ?)
                """, (default_username, hashed_password, "admin", None))
                self.conn.commit()
                print(f"Default admin user '{default_username}' created.")
            else:
                print("Admin user already exists.")
        except sqlite3.Error as e:
            print(f"Error creating default admin: {e}")

    # --- Metode baru untuk membuat anggota default dan user anggota ---
    def create_default_members_and_users(self):
        """Add default members and link them to user accounts if members table is empty."""
        try:
            self.cursor.execute("SELECT COUNT(*) FROM members")
            member_count = self.cursor.fetchone()[0]
            if member_count == 0:
                new_members_data = [
                    ("Sanjaya", "Jl. Cemara No. 10", "08112233445", "sanjaya@email.com", "sanjaya", "sanjaya123"),
                    ("Ayu Rianti", "Jl. Anggrek No. 25", "08223344556", "ayu.rianti@email.com", "ayurianti", "ayu123"),
                    ("Muhammad Abdullah Fikri", "Jl. Merpati No. 7", "08334455667", "fikri.m@email.com", "fikri", "fikri123")
                ]

                for name, address, phone, email, username, password in new_members_data:
                    self.cursor.execute("SELECT id FROM members WHERE name = ? OR email = ?", (name, email))
                    existing_member = self.cursor.fetchone()

                    if not existing_member:
                        self.cursor.execute("""
                            INSERT INTO members (name, address, phone, email)
                            VALUES (?, ?, ?, ?)
                        """, (name, address, phone, email))
                        member_id = self.cursor.lastrowid
                        self.conn.commit()
                        print(f"Anggota '{name}' dibuat dengan ID: {member_id}")

                        # Cek apakah user untuk anggota ini sudah ada berdasarkan member_id
                        self.cursor.execute("SELECT id FROM users WHERE member_id = ?", (member_id,))
                        existing_user = self.cursor.fetchone()

                        if not existing_user:
                            hashed_password = self.hash_password(password)
                            self.cursor.execute("""
                                INSERT INTO users (username, password_hash, role, member_id)
                                VALUES (?, ?, ?, ?)
                            """, (username, hashed_password, "member", member_id))
                            self.conn.commit()
                            print(f"User anggota '{username}' created and linked to member ID {member_id}.")
                        else:
                            print(f"User untuk anggota '{name}' (ID {member_id}) sudah ada.")
                    else:
                        print(f"Anggota '{name}' atau '{email}' sudah ada, tidak perlu dibuat ulang.")
            else:
                print("Default members already exist.")
        except sqlite3.Error as e:
            print(f"Error creating default members and users: {e}")

    # --- Metode baru untuk membuat buku default ---
    def create_default_books(self):
        """Add default books if books table is empty."""
        try:
            self.cursor.execute("SELECT COUNT(*) FROM books")
            book_count = self.cursor.fetchone()[0]
            if book_count == 0:
                sample_books = [
                    ("Sejarah Dunia Kuno", "Penulis Sejarah 1", "978-602-03-3290-0", "Sejarah", 5, 5),
                    ("Pengantar Ilmu Komputer", "Penulis Ilmu 1", "978-979-433-760-3", "Ilmu Pengetahuan", 8, 8),
                    ("Fisika Dasar Jilid 1", "Penulis Ilmu 2", "978-979-099-521-9", "Ilmu Pengetahuan", 6, 6),
                    ("Novel Misteri Pulau Terpencil", "Penulis Fiksi 1", "978-602-04-2345-1", "Fiksi", 10, 10),
                    ("Kumpulan Puisi Senja", "Penyair 1", "978-979-22-8765-4", "Sastra", 4, 4),
                    ("Teknologi Blockchain", "Penulis Teknologi 1", "978-602-423-111-2", "Teknologi", 7, 7),
                    ("Ekonomi Makro", "Penulis Ekonomi 1", "978-979-061-123-4", "Ekonomi", 5, 5),
                    ("Biologi Sel", "Penulis Ilmu 3", "978-979-044-567-8", "Ilmu Pengetahuan", 6, 6),
                    ("Sejarah Indonesia Modern", "Penulis Sejarah 2", "978-602-876-543-2", "Sejarah", 7, 7),
                    ("Dasar-dasar Desain Grafis", "Penulis Seni 1", "978-979-123-456-7", "Seni", 5, 5),
                    ("Algoritma dan Struktur Data", "Penulis Ilmu 4", "978-979-345-678-9", "Ilmu Pengetahuan", 9, 9),
                    ("Filsafat Ilmu", "Penulis Filsafat 1", "978-602-987-654-3", "Filsafat", 4, 4),
                    ("Geografi Regional Asia Tenggara", "Penulis Geografi 1", "978-979-234-567-8", "Geografi", 3, 3),
                    ("Kimia Organik", "Penulis Ilmu 5", "978-979-876-543-2", "Ilmu Pengetahuan", 5, 5),
                    ("Arkeologi Indonesia", "Penulis Sejarah 3", "978-602-109-876-5", "Sejarah", 4, 4),
                ]
                self.cursor.executemany("""
                    INSERT INTO books (title, author, isbn, category, stock, available)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, sample_books)
                self.conn.commit()
                print(f"{len(sample_books)} sample books added.")
            else:
                print("Default books already exist.")
        except sqlite3.Error as e:
            print(f"Error creating default books: {e}")


    # --- User Authentication Methods ---
    def get_user(self, username):
        """Retrieve user details by username."""
        try:
            self.cursor.execute("SELECT id, username, password_hash, role, member_id FROM users WHERE username = ?", (username,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error fetching user: {e}")
            return None

    def get_user_by_id(self, user_id):
        self.cursor.execute("SELECT id, username, password_hash, role, member_id FROM users WHERE id = ?", (user_id,))
        return self.cursor.fetchone()

    def get_user_by_username(self, username):
        """Retrieve user details by username, used in app.py for current_user_id."""
        return self.get_user(username)

    def add_user(self, username, password, role, member_id=None):
        hashed_password = self.hash_password(password)
        try:
            self.cursor.execute("INSERT INTO users (username, password_hash, role, member_id) VALUES (?, ?, ?, ?)",
                                (username, hashed_password, role, member_id))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            print(f"Username '{username}' already exists or invalid member_id.")
            return False
        except sqlite3.Error as e:
            print(f"Error adding user: {e}")
            return False

    def update_user(self, user_id, new_username=None, new_password=None, new_role=None, new_member_id=None):
        update_fields = []
        params = []
        if new_username:
            update_fields.append("username = ?")
            params.append(new_username)
        if new_password:
            hashed_password = self.hash_password(new_password)
            update_fields.append("password_hash = ?")
            params.append(hashed_password)
        if new_role:
            update_fields.append("role = ?")
            params.append(new_role)
        if new_member_id is not None:
            update_fields.append("member_id = ?")
            params.append(new_member_id)
        
        if not update_fields:
            return False 

        params.append(user_id)
        query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = ?"
        try:
            self.cursor.execute(query, tuple(params))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            print("Update failed: Username already exists or invalid member_id.")
            return False
        except sqlite3.Error as e:
            print(f"Error updating user: {e}")
            return False

    def delete_user(self, user_id):
        try:
            self.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting user: {e}")
            return False

    # --- Member Management Methods ---
    def add_member(self, name, address, phone, email):
        try:
            self.cursor.execute("INSERT INTO members (name, address, phone, email) VALUES (?, ?, ?, ?)",
                                (name, address, phone, email))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError as e:
            print(f"Error adding member (phone or email might exist): {e}")
            return None
        except sqlite3.Error as e:
            print(f"Error adding member: {e}")
            return None

    def get_member(self, member_id):
        self.cursor.execute("SELECT id, name, address, phone, email FROM members WHERE id = ?", (member_id,))
        return self.cursor.fetchone()
    
    def get_member_by_phone_or_email(self, contact):
        self.cursor.execute("SELECT id, name, address, phone, email FROM members WHERE phone = ? OR email = ?", (contact, contact))
        return self.cursor.fetchone()

    def get_all_members(self):
        self.cursor.execute("SELECT id, name, address, phone, email FROM members")
        return self.cursor.fetchall()

    def update_member(self, member_id, name=None, address=None, phone=None, email=None):
        update_fields = []
        params = []
        if name:
            update_fields.append("name = ?")
            params.append(name)
        if address:
            update_fields.append("address = ?")
            params.append(address)
        if phone:
            update_fields.append("phone = ?")
            params.append(phone)
        if email:
            update_fields.append("email = ?")
            params.append(email)
        
        if not update_fields:
            return False

        params.append(member_id)
        query = f"UPDATE members SET {', '.join(update_fields)} WHERE id = ?"
        try:
            self.cursor.execute(query, tuple(params))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Update failed: Phone or email already exists for another member: {e}")
            return False
        except sqlite3.Error as e:
            print(f"Error updating member: {e}")
            return False

    def delete_member(self, member_id):
        try:
            self.cursor.execute("DELETE FROM members WHERE id = ?", (member_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting member: {e}")
            return False

    # --- Book Management Methods ---
    def add_book(self, title, author, isbn, category, stock, available):
        try:
            self.cursor.execute("INSERT INTO books (title, author, isbn, category, stock, available) VALUES (?, ?, ?, ?, ?, ?)",
                                (title, author, isbn, category, stock, available))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Book with ISBN '{isbn}' already exists: {e}")
            return False
        except sqlite3.Error as e:
            print(f"Error adding book: {e}")
            return False

    def get_all_books(self):
        self.cursor.execute("SELECT id, title, author, isbn, category, stock, available FROM books")
        return self.cursor.fetchall()

    def get_book_by_id(self, book_id):
        self.cursor.execute("SELECT id, title, author, isbn, category, stock, available FROM books WHERE id = ?", (book_id,))
        return self.cursor.fetchone()

    def get_book_by_isbn(self, isbn):
        self.cursor.execute("SELECT id, title, author, isbn, category, stock, available FROM books WHERE isbn = ?", (isbn,))
        return self.cursor.fetchone()

    def update_book(self, book_id, title=None, author=None, isbn=None, category=None, stock=None, available=None):
        update_fields = []
        params = []
        if title:
            update_fields.append("title = ?")
            params.append(title)
        if author:
            update_fields.append("author = ?")
            params.append(author)
        if isbn:
            update_fields.append("isbn = ?")
            params.append(isbn)
        if category:
            update_fields.append("category = ?")
            params.append(category)
        if stock is not None:
            update_fields.append("stock = ?")
            params.append(stock)
        if available is not None:
            update_fields.append("available = ?")
            params.append(available)
        
        if not update_fields:
            return False

        params.append(book_id)
        query = f"UPDATE books SET {', '.join(update_fields)} WHERE id = ?"
        try:
            self.cursor.execute(query, tuple(params))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Update failed: ISBN '{isbn}' already exists: {e}")
            return False
        except sqlite3.Error as e:
            print(f"Error updating book: {e}")
            return False

    def delete_book(self, book_id):
        try:
            self.cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting book: {e}")
            return False

    # --- Borrowing Management Methods ---
    def borrow_book(self, book_id, member_id):
        borrow_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Contoh: Tenggat pengembalian 14 hari dari tanggal pinjam
        due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d %H:%M:%S") 
        try:
            # Periksa ketersediaan buku
            self.cursor.execute("SELECT available FROM books WHERE id = ?", (book_id,))
            available_qty = self.cursor.fetchone()[0]
            if available_qty > 0:
                self.cursor.execute("INSERT INTO borrowings (book_id, member_id, borrow_date, due_date, status, fine_amount) VALUES (?, ?, ?, ?, ?, ?)",
                                    (book_id, member_id, borrow_date, due_date, 'Borrowed', 0.0))
                self.conn.commit()
                # Kurangi jumlah buku yang tersedia
                self.cursor.execute("UPDATE books SET available = available - 1 WHERE id = ?", (book_id,))
                self.conn.commit()
                return True
            else:
                print("Book not available for borrowing.")
                return False
        except sqlite3.Error as e:
            print(f"Error borrowing book: {e}")
            return False

    def return_book(self, borrowing_id):
        return_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.cursor.execute("SELECT book_id, due_date FROM borrowings WHERE id = ?", (borrowing_id,))
            borrowing_info = self.cursor.fetchone()
            if not borrowing_info:
                print("Borrowing record not found.")
                return False
            
            book_id, due_date_str = borrowing_info
            fine = 0.0
            
            # Hitung denda jika ada
            due_date_dt = datetime.strptime(due_date_str, "%Y-%m-%d %H:%M:%S")
            return_date_dt = datetime.strptime(return_date, "%Y-%m-%d %H:%M:%S")

            if return_date_dt > due_date_dt:
                days_overdue = (return_date_dt - due_date_dt).days
                fine = days_overdue * FINE_PER_DAY
                print(f"Book overdue by {days_overdue} days. Fine: {fine}")

            self.cursor.execute("UPDATE borrowings SET return_date = ?, status = 'Returned', fine_amount = ? WHERE id = ?",
                                (return_date, fine, borrowing_id))
            self.conn.commit()

            # Tambah jumlah buku yang tersedia
            self.cursor.execute("UPDATE books SET available = available + 1 WHERE id = ?", (book_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error returning book: {e}")
            return False

    def get_borrowings_by_status(self, status):
        self.cursor.execute("""
            SELECT 
                b.id, bk.title, m.name, b.borrow_date, b.return_date, b.status, b.fine_amount
            FROM borrowings b
            JOIN books bk ON b.book_id = bk.id
            JOIN members m ON b.member_id = m.id
            WHERE b.status = ?
        """, (status,))
        return self.cursor.fetchall()
    
    def get_all_borrowings(self):
        self.cursor.execute("""
            SELECT 
                b.id, bk.title, m.name, b.borrow_date, b.return_date, b.status, b.fine_amount
            FROM borrowings b
            JOIN books bk ON b.book_id = bk.id
            JOIN members m ON b.member_id = m.id
        """)
        return self.cursor.fetchall()

    def get_member_borrowings(self, member_id):
        """Get all borrowings for a specific member."""
        self.cursor.execute("""
            SELECT 
                b.id, bk.title, bk.author, b.borrow_date, b.return_date, b.status, b.fine_amount
            FROM borrowings b
            JOIN books bk ON b.book_id = bk.id
            WHERE b.member_id = ?
            ORDER BY b.borrow_date DESC
        """, (member_id,))
        return self.cursor.fetchall()

    def get_overdue_borrowings(self):
        """Get all overdue borrowings."""
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("""
            SELECT 
                b.id, bk.title, m.name, b.borrow_date, b.return_date, b.status, b.fine_amount
            FROM borrowings b
            JOIN books bk ON b.book_id = bk.id
            JOIN members m ON b.member_id = m.id
            WHERE b.status = 'Borrowed' AND b.due_date < ?
        """, (current_date,))
        return self.cursor.fetchall()


# Example usage (for testing purposes, can be removed later)
if __name__ == "__main__":
    db = Database()

    print("\n--- Daftar Anggota ---")
    db.cursor.execute("SELECT id, name, email, phone FROM members")
    for row in db.cursor.fetchall():
        print(row)

    print("\n--- Daftar Pengguna (Users) ---")
    db.cursor.execute("SELECT id, username, role, member_id FROM users")
    for row in db.cursor.fetchall():
        print(row)

    print("\n--- Daftar Buku ---")
    db.cursor.execute("SELECT id, title, stock, available FROM books")
    for row in db.cursor.fetchall():
        print(row)

    db.disconnect()