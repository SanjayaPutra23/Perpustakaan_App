from reportlab.lib.pagesizes import A7 
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
import os
from tkinter import filedialog, messagebox

def generate_borrowing_receipt(borrowing_details):
    """
    Menghasilkan struk peminjaman dalam format PDF dengan desain yang lebih menarik.

    Args:
        borrowing_details (dict): Dictionary berisi detail peminjaman.
            Harus berisi keys: 'borrowing_id', 'book_title', 'member_name',
            'borrow_date', 'due_date' (opsional), 'library_name' (opsional).
    """
    try:
        library_name = borrowing_details.get('library_name', "Perpustakaan Umum")
        borrowing_id = borrowing_details.get('borrowing_id', 'N/A')
        book_title = borrowing_details.get('book_title', 'N/A')
        member_name = borrowing_details.get('member_name', 'N/A')
        borrow_date = borrowing_details.get('borrow_date', 'N/A')
        due_date = borrowing_details.get('due_date', 'N/A') 

        # Minta pengguna memilih lokasi penyimpanan file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Simpan Struk Peminjaman Sebagai...",
            initialfile=f"struk_peminjaman_{borrowing_id}.pdf"
        )

        if not file_path:
            messagebox.showinfo("Batal", "Pembuatan struk dibatalkan.")
            return None

        # Dokumen PDF
        doc = SimpleDocTemplate(file_path, pagesize=A7,
                                rightMargin=5*mm, leftMargin=5*mm,
                                topMargin=5*mm, bottomMargin=5*mm)
        story = []
        styles = getSampleStyleSheet()

        # --- Custom Styles untuk Teks ---
        # Gaya untuk judul perpustakaan
        styles.add(ParagraphStyle(name='LibraryTitle',
                                  parent=styles['h1'],
                                  fontName='Helvetica-Bold',
                                  fontSize=12, 
                                  alignment=1,
                                  textColor=colors.blue))

        # Gaya untuk sub judul struk
        styles.add(ParagraphStyle(name='ReceiptHeader',
                                  parent=styles['h2'],
                                  fontName='Helvetica-Bold',
                                  fontSize=10, 
                                  alignment=1, 
                                  textColor=colors.darkgreen))

        # Gaya untuk detail tabel
        styles.add(ParagraphStyle(name='DetailLabel',
                                  parent=styles['Normal'],
                                  fontName='Helvetica-Bold',
                                  fontSize=8, 
                                  textColor=colors.HexColor('#4A4A4A')))

        styles.add(ParagraphStyle(name='DetailValue',
                                  parent=styles['Normal'],
                                  fontName='Helvetica',
                                  fontSize=8,
                                  textColor=colors.HexColor('#000000'))) 

        # Gaya untuk pesan penutup
        styles.add(ParagraphStyle(name='ClosingMessage',
                                  parent=styles['Normal'],
                                  fontName='Helvetica-Oblique',
                                  fontSize=7,
                                  alignment=1,
                                  textColor=colors.grey))

        # --- Konten Struk ---
        # Judul Struk
        story.append(Paragraph(library_name, styles['LibraryTitle']))
        story.append(Paragraph("Struk Peminjaman Buku", styles['ReceiptHeader']))
        story.append(Spacer(1, 4*mm))

        # Detail Peminjaman dalam bentuk tabel
        data = [
            [Paragraph("ID Peminjaman:", styles['DetailLabel']), Paragraph(str(borrowing_id), styles['DetailValue'])],
            [Paragraph("Nama Anggota:", styles['DetailLabel']), Paragraph(member_name, styles['DetailValue'])],
            [Paragraph("Judul Buku:", styles['DetailLabel']), Paragraph(book_title, styles['DetailValue'])],
            [Paragraph("Tanggal Pinjam:", styles['DetailLabel']), Paragraph(borrow_date, styles['DetailValue'])],
            [Paragraph("Jatuh Tempo:", styles['DetailLabel']), Paragraph(due_date, styles['DetailValue'])],
        ]

        # Gaya Tabel
        table_style = TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#4A4A4A')), 
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#000000')), 
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2*mm),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.HexColor('#E0E0E0')), 
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#B0B0B0')), 
        ])

        table = Table(data, colWidths=[25*mm, 45*mm]) 
        table.setStyle(table_style)
        story.append(table)
        story.append(Spacer(1, 5*mm))

        # Pesan Tambahan dengan Emotikon/Simbol
        story.append(Paragraph("Terima kasih telah meminjam! 😊", styles['ClosingMessage']))
        story.append(Paragraph("Harap kembalikan tepat waktu untuk menghindari denda. ⏳", styles['ClosingMessage']))
        story.append(Spacer(1, 2*mm))
        story.append(Paragraph("--- Perpustakaan Digital ---", styles['ClosingMessage'])) 

        doc.build(story)
        messagebox.showinfo("Sukses", f"Struk peminjaman berhasil disimpan sebagai:\n{file_path}")
        return file_path

    except Exception as e:
        messagebox.showerror("Error Membuat PDF", f"Gagal membuat struk PDF: {e}")
        return None

if __name__ == '__main__':
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()

    test_details = {
        'borrowing_id': 'PJM20240528001',
        'book_title': 'Seni Memahami Python Lanjutan',
        'member_name': 'Sanjaya',
        'borrow_date': '2025-05-28',
        'due_date': '2025-06-04', 
        'library_name': 'Perpustakaan Jaya'
    }
    generate_borrowing_receipt(test_details)

    root.destroy()
    
    print("\nFungsi generate_borrowing_receipt siap digunakan.")
    print("Pastikan ReportLab terinstal: pip install reportlab")
    print("Jalankan dari aplikasi utama untuk fungsionalitas penuh filedialog.")