import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import csv
from datetime import datetime
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors

class ReportFrame(ttk.Frame):
    def __init__(self, parent, controller, style_instance):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = self.controller.db
        self.report_data = []

        # --- Style Configuration ---
        self.style = style_instance

        # Title Style
        self.style.configure("ReportTitle.TLabel", font=("Arial", 18, "bold"), foreground="#007BFF")

        # Filter Frame Style
        self.style.configure("Filter.TLabelframe.Label", font=("Arial", 11, "bold"), foreground="#333333")
        self.style.configure("Filter.TLabelframe", background="#F8F8F8", relief="solid", borderwidth=1)
        self.style.configure("TCombobox", fieldbackground="#FFFFFF", background="#FFFFFF")

        # Button Styles (Ini harusnya aman dan tidak konflik dengan Treeview)
        self.style.configure("ReportButton.TButton",
                             font=("Arial", 10, "bold"),
                             padding=8,
                             relief="flat")

        self.style.configure("Generate.ReportButton.TButton",
                             background="#28A745",
                             foreground="black")
        self.style.map("Generate.ReportButton.TButton",
                       background=[('active', '#218838')])

        self.style.configure("ExportCSV.ReportButton.TButton",
                             background="#17A2B8",
                             foreground="black")
        self.style.map("ExportCSV.ReportButton.TButton",
                       background=[('active', '#138496')])

        self.style.configure("ExportPDF.ReportButton.TButton",
                             background="#DC3545",
                             foreground="black")
        self.style.map("ExportPDF.ReportButton.TButton",
                       background=[('active', '#C82333')])


        # Frame untuk Judul
        title_frame = ttk.Frame(self)
        title_frame.pack(pady=10)
        lbl_title = ttk.Label(title_frame, text="📊 Laporan Peminjaman & Pengembalian", style="ReportTitle.TLabel")
        lbl_title.pack()

        # Frame untuk Filter
        filter_frame = ttk.LabelFrame(self, text="🔍 Filter Laporan", style="Filter.TLabelframe")
        filter_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(filter_frame, text="Tanggal Mulai (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_start_date = ttk.Entry(filter_frame, width=15)
        self.entry_start_date.grid(row=0, column=1, padx=5, pady=5)
        self.entry_start_date.insert(0, datetime.now().strftime("%Y-%m-01"))

        ttk.Label(filter_frame, text="Tanggal Akhir (YYYY-MM-DD):").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_end_date = ttk.Entry(filter_frame, width=15)
        self.entry_end_date.grid(row=0, column=3, padx=5, pady=5)
        self.entry_end_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        ttk.Label(filter_frame, text="Status:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.combo_status = ttk.Combobox(filter_frame, values=["Semua", "Borrowed", "Returned"], width=12, state="readonly")
        self.combo_status.grid(row=1, column=1, padx=5, pady=5)
        self.combo_status.set("Semua")

        btn_generate_report = ttk.Button(filter_frame, text="📈 Tampilkan Laporan", command=self.generate_report, style="Generate.ReportButton.TButton")
        btn_generate_report.grid(row=1, column=2, columnspan=2, padx=5, pady=10)


        # Frame dan Tabel untuk Menampilkan Data Laporan (Treeview)
        table_frame = ttk.Frame(self)
        table_frame.pack(pady=10, padx=10, fill="both", expand=True)

        scrollbar_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        scrollbar_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)

        self.tree_report = ttk.Treeview(table_frame,
                                        columns=("ID", "Judul Buku", "Nama Anggota", "Tgl Pinjam", "Tgl Kembali", "Status"),
                                        show="headings",
                                        yscrollcommand=scrollbar_y.set,
                                        xscrollcommand=scrollbar_x.set)

        # Jika Anda ingin tag kustom untuk warna baris (misalnya untuk status), definisikan di sini:
        self.tree_report.tag_configure('borrowed_tag', foreground='blue', font=('Arial', 9))
        self.tree_report.tag_configure('returned_tag', foreground='green', font=('Arial', 9))
        self.tree_report.tag_configure('overdue_tag', foreground='red', font=('Arial', 9, 'bold'))

        scrollbar_y.config(command=self.tree_report.yview)
        scrollbar_x.config(command=self.tree_report.xview)

        # Define headings (Ini aman)
        self.tree_report.heading("ID", text="ID Pinjam")
        self.tree_report.heading("Judul Buku", text="Judul Buku")
        self.tree_report.heading("Nama Anggota", text="Nama Anggota")
        self.tree_report.heading("Tgl Pinjam", text="Tgl Pinjam")
        self.tree_report.heading("Tgl Kembali", text="Tgl Kembali")
        self.tree_report.heading("Status", text="Status")

        # Define column widths (Ini aman)
        self.tree_report.column("ID", width=80, anchor="center")
        self.tree_report.column("Judul Buku", width=200)
        self.tree_report.column("Nama Anggota", width=150)
        self.tree_report.column("Tgl Pinjam", width=100, anchor="center")
        self.tree_report.column("Tgl Kembali", width=100, anchor="center")
        self.tree_report.column("Status", width=80, anchor="center")

        self.tree_report.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Frame untuk Tombol Ekspor
        export_button_frame = ttk.Frame(self)
        export_button_frame.pack(pady=10)

        self.btn_export_csv = ttk.Button(export_button_frame, text="📄 Ekspor ke CSV", command=self.export_to_csv, state=tk.DISABLED, style="ExportCSV.ReportButton.TButton")
        self.btn_export_csv.grid(row=0, column=0, padx=5)

        self.btn_export_pdf = ttk.Button(export_button_frame, text="🖨️ Ekspor ke PDF", command=self.export_to_pdf, state=tk.DISABLED, style="ExportPDF.ReportButton.TButton")
        self.btn_export_pdf.grid(row=0, column=1, padx=5)

    def generate_report(self):
        start_date_str = self.entry_start_date.get()
        end_date_str = self.entry_end_date.get()
        status_filter = self.combo_status.get()

        try:
            datetime.strptime(start_date_str, "%Y-%m-%d")
            datetime.strptime(end_date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Format Tanggal Salah", "Format tanggal harusุงเทพ-MM-DD.")
            return

        for item in self.tree_report.get_children():
            self.tree_report.delete(item)
        self.report_data = []

        try:
            query = """
                SELECT
                    b.id, bo.title, m.name, b.borrow_date, b.return_date, b.status
                FROM
                    borrowings b
                JOIN
                    books bo ON b.book_id = bo.id
                JOIN
                    members m ON b.member_id = m.id
                WHERE
                    b.borrow_date BETWEEN ? AND ?
            """
            params = [start_date_str, end_date_str]

            if status_filter != "Semua":
                query += " AND b.status = ?"
                params.append(status_filter)

            query += " ORDER BY b.borrow_date DESC"

            self.db.cursor.execute(query, tuple(params))
            rows = self.db.cursor.fetchall()

            if not rows:
                messagebox.showinfo("Laporan Kosong", "Tidak ada data peminjaman untuk filter yang dipilih. 🤷‍♀️")
                self.btn_export_csv.config(state=tk.DISABLED)
                self.btn_export_pdf.config(state=tk.DISABLED)
                return

            for row in rows:
                self.tree_report.insert("", tk.END, values=row)
                self.report_data.append(row)

            messagebox.showinfo("Laporan Siap", "Laporan berhasil dibuat! ✅")
            self.btn_export_csv.config(state=tk.NORMAL)
            self.btn_export_pdf.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Error Database", f"Gagal menghasilkan laporan: {e}")
            self.btn_export_csv.config(state=tk.DISABLED)
            self.btn_export_pdf.config(state=tk.DISABLED)

    def export_to_csv(self):
        """Mengekspor data laporan saat ini ke file CSV."""
        if not self.report_data:
            messagebox.showwarning("Tidak Ada Data", "Tidak ada data laporan untuk diekspor. 🚫")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Simpan Laporan CSV Sebagai...",
            initialfile="laporan_peminjaman.csv"
        )

        if not file_path:
            return

        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                headers = ["ID Pinjam", "Judul Buku", "Nama Anggota", "Tgl Pinjam", "Tgl Kembali", "Status"]
                csv_writer.writerow(headers)
                csv_writer.writerows(self.report_data)
            messagebox.showinfo("Sukses", f"Laporan berhasil diekspor ke CSV:\\n{file_path} 🎉")
        except Exception as e:
            messagebox.showerror("Error Ekspor CSV", f"Gagal mengekspor ke CSV: {e} ❌")

    def export_to_pdf(self):
        """Mengekspor data laporan saat ini ke file PDF."""
        if not self.report_data:
            messagebox.showwarning("Tidak Ada Data", "Tidak ada data laporan untuk diekspor. 🚫")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Simpan Laporan PDF Sebagai...",
            initialfile="laporan_peminjaman.pdf"
        )

        if not file_path:
            return

        try:
            doc = SimpleDocTemplate(file_path, pagesize=landscape(letter),
                                    rightMargin=0.5*inch, leftMargin=0.5*inch,
                                    topMargin=0.5*inch, bottomMargin=0.5*inch)
            styles = getSampleStyleSheet()
            story = []

            story.append(Paragraph("Laporan Peminjaman & Pengembalian", styles['h1']))
            story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph(f"Periode: {self.entry_start_date.get()} s/d {self.entry_end_date.get()}", styles['Normal']))
            story.append(Paragraph(f"Status Filter: {self.combo_status.get()}", styles['Normal']))
            story.append(Spacer(1, 0.3*inch))

            table_data = [["ID Pinjam", "Judul Buku", "Nama Anggota", "Tgl Pinjam", "Tgl Kembali", "Status"]]
            for row in self.report_data:
                table_data.append(list(row))

            report_table = Table(table_data, repeatRows=1)
            report_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0,0), (-1,-1), 1, colors.black)
            ]))
            story.append(report_table)

            doc.build(story)
            messagebox.showinfo("Sukses", f"Laporan berhasil diekspor ke PDF:\n{file_path} 📄")

        except Exception as e:
            messagebox.showerror("Error Ekspor PDF", f"Gagal mengekspor ke PDF: {e} ❌")


    def on_show(self):
        """Dipanggil saat frame ini ditampilkan."""
        print("Report frame shown.")
        for item in self.tree_report.get_children():
            self.tree_report.delete(item)
        self.report_data = []
        self.btn_export_csv.config(state=tk.DISABLED)
        self.btn_export_pdf.config(state=tk.DISABLED)
        self.entry_start_date.delete(0, tk.END)
        self.entry_start_date.insert(0, datetime.now().strftime("%Y-%m-01"))
        self.entry_end_date.delete(0, tk.END)
        self.entry_end_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.combo_status.set("Semua")