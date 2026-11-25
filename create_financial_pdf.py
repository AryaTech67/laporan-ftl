import os
import shutil
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Running Header (pages > 1)
        if self._pageNumber > 1:
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(36, A4[1] - 30, A4[0] - 36, A4[1] - 30)
            self.drawString(36, A4[1] - 25, "FOR THE LITTLE INDONESIA • Panduan Sumber Data & Rumus Finansial Portal Rekap v3.9")
        
        # Running Footer
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(36, 36, A4[0] - 36, 36)
        
        footer_text_left = "Dokumen SOP Finansial Internal • For The Little Indonesia"
        footer_text_right = f"Halaman {self._pageNumber} dari {page_count}"
        
        self.drawString(36, 24, footer_text_left)
        self.drawRightString(A4[0] - 36, 24, footer_text_right)
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=40,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()
    
    # Custom Brand Colors
    c_primary = colors.HexColor("#264D3B")     # Deep Forest Green
    c_sage = colors.HexColor("#738a7a")        # Sage Green FTL
    c_soft_mint = colors.HexColor("#abcbb2")   # Soft Mint
    c_yellow = colors.HexColor("#fce9a1")      # Butter Yellow
    c_dark = colors.HexColor("#0f172a")        # Slate 900
    c_text = colors.HexColor("#1e293b")        # Slate 800
    c_muted = colors.HexColor("#64748b")       # Slate 500
    c_bg_box = colors.HexColor("#f8fafc")      # Slate 50
    c_rose = colors.HexColor("#e11d48")        # Rose Red (Diskon & Batal)
    c_emerald = colors.HexColor("#059669")     # Emerald (Omset Bersih)
    c_indigo = colors.HexColor("#4f46e5")      # Indigo (HPP)
    c_blue = colors.HexColor("#2563eb")        # Blue (Laba)

    # Paragraph Styles
    style_title = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=c_primary,
        spaceAfter=2
    )

    style_subtitle = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#8D6E54"),
        spaceAfter=0
    )

    style_h2 = ParagraphStyle(
        'Heading2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=c_primary,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_text,
        spaceAfter=4
    )

    style_body_bold = ParagraphStyle(
        'BodyBoldCustom',
        parent=style_body,
        fontName='Helvetica-Bold'
    )

    style_callout = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_text
    )

    style_table_header = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=1
    )

    style_td = ParagraphStyle(
        'TD',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=c_text
    )

    style_td_bold = ParagraphStyle(
        'TDBold',
        parent=style_td,
        fontName='Helvetica-Bold'
    )

    style_formula = ParagraphStyle(
        'FormulaText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=c_dark
    )

    story = []

    # 1. HEADER SECTION
    logo_path = "logo-ftl.png"
    has_logo = os.path.exists(logo_path)
    
    header_data = [
        [
            Image(logo_path, width=1.3*cm, height=1.3*cm) if has_logo else "",
            [
                Paragraph("FOR THE LITTLE INDONESIA", style_title),
                Paragraph("PANDUAN SUMBER DATA & RUMUS KALKULASI FINANSIAL", style_subtitle),
                Paragraph("Portal Rekapitulasi Laporan Penjualan (Shopee & TikTok) • Standar Operasional v3.9", ParagraphStyle('MetaSub', fontName='Helvetica', fontSize=7.5, leading=10, textColor=c_muted))
            ],
            [
                Paragraph("<b>DOKUMEN RESMI</b>", ParagraphStyle('RMeta', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=c_primary, alignment=2)),
                Paragraph("Status: Terverifikasi", ParagraphStyle('RMeta2', fontName='Helvetica', fontSize=7.5, leading=9, textColor=c_muted, alignment=2)),
                Paragraph("Website: <u>laporanftl.vercel.app</u>", ParagraphStyle('RMeta3', fontName='Helvetica', fontSize=7.5, leading=9, textColor=colors.HexColor("#2563eb"), alignment=2))
            ]
        ]
    ]

    header_table = Table(header_data, colWidths=[1.5*cm, 12.0*cm, 4.5*cm])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(header_table)
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=4, spaceAfter=8))

    # 2. EXECUTIVE SUMMARY BOX
    summary_text = (
        "<b>Tujuan Dokumen:</b> Dokumen ini memberikan panduan resmi mengenai asal-usul kolom data mentah dari "
        "file Excel/CSV (Shopee Seller Centre & TikTok Shop Seller Center) serta logika rumus matematika yang digunakan "
        "dalam menghitung <b>Omset Kotor, Total Diskon, Omset Bersih, HPP (Modal Barang), dan Estimasi Laba Bersih</b> "
        "pada portal rekapitulasi For The Little (FTL). Seluruh perhitungan bersifat transparan dan dapat diaudit secara riil."
    )
    summary_table = Table([[Paragraph(summary_text, style_callout)]], colWidths=[18.0*cm])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f4f7f5")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#d2ded6")),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 8))

    # 3. MASTER TABLE: 6 METRIK FINANSIAL UTAMA
    story.append(Paragraph("1. TABEL SUMBER KOLOM & FORMULA 6 INDIKATOR KEUANGAN", style_h2))
    
    table_fin_data = [
        [
            Paragraph("No", style_table_header),
            Paragraph("Indikator Finansial", style_table_header),
            Paragraph("Sumber Laporan Shopee", style_table_header),
            Paragraph("Sumber Laporan TikTok", style_table_header),
            Paragraph("Rumus Perhitungan", style_table_header),
            Paragraph("Arti / Kegunaan", style_table_header)
        ],
        [
            Paragraph("1", style_td_bold),
            Paragraph("<b>OMSET KOTOR</b><br/><font color='#64748b'>(Gross Sales)</font>", style_td),
            Paragraph("Kolom: <b>Subtotal Pesanan</b><br/>(Col 24 / Harga Toko)", style_td),
            Paragraph("Kolom: <b>SKU Subtotal Before Discount</b> (Col 14)", style_td),
            Paragraph("<code>Subtotal Pesanan</code>", style_td_bold),
            Paragraph("Total nilai transaksi sebelum dipotong diskon/voucher apapun.", style_td)
        ],
        [
            Paragraph("2", style_td_bold),
            Paragraph("<b>TOTAL DISKON</b><br/><font color='#e11d48'>(Potongan Toko & Platform)</font>", style_td),
            Paragraph("Selisih Riil Toko:<br/><b>Subtotal Pesanan − Total Pembayaran</b>", style_td),
            Paragraph("Penjumlahan Kolom:<br/><b>SKU Platform Disc</b> (Col 15) + <b>SKU Seller Disc</b> (Col 16)", style_td),
            Paragraph("<font color='#e11d48'>Kotor − Bersih</font><br/><i>atau</i> Platform + Seller Disc", style_td_bold),
            Paragraph("Total seluruh potongan voucher toko dan subsidi platform.", style_td)
        ],
        [
            Paragraph("3", style_td_bold),
            Paragraph("<b>OMSET BERSIH</b><br/><font color='#059669'>(Net Cash-In)</font>", style_td),
            Paragraph("Kolom: <b>Total Pembayaran</b><br/>(Col 42 / Uang Riil Pembeli)", style_td),
            Paragraph("Kolom: <b>Order Amount</b><br/>(Col 30 / Uang Riil Pembeli)", style_td),
            Paragraph("<font color='#059669'>Omset Kotor − Total Diskon</font>", style_td_bold),
            Paragraph("Uang riil yang dibayar pembeli dan masuk ke rekening toko.", style_td)
        ],
        [
            Paragraph("4", style_td_bold),
            Paragraph("<b>TOTAL HPP</b><br/><font color='#4f46e5'>(Modal Barang)</font>", style_td),
            Paragraph("Qty Pesanan 'Selesai' × HPP Satuan", style_td),
            Paragraph("Qty Pesanan 'Selesai' × HPP Satuan", style_td),
            Paragraph("<font color='#4f46e5'>Qty Selesai × Rp 25.000</font><br/><i>(rate HPP bisa diatur)</i>", style_td_bold),
            Paragraph("Total modal produk fisik yang keluar dari gudang (pesanan sukses).", style_td)
        ],
        [
            Paragraph("5", style_td_bold),
            Paragraph("<b>ESTIMASI LABA</b><br/><font color='#2563eb'>(Profit Margin)</font>", style_td),
            Paragraph("Omset Bersih Shopee − HPP", style_td),
            Paragraph("Omset Bersih TikTok − HPP", style_td),
            Paragraph("<font color='#2563eb'>Omset Bersih − Total HPP</font>", style_td_bold),
            Paragraph("Keuntungan kotor toko setelah dipotong modal pokok produksi.", style_td)
        ],
        [
            Paragraph("6", style_td_bold),
            Paragraph("<b>TOTAL BATAL</b><br/><font color='#e11d48'>(Loss Melayang)</font>", style_td),
            Paragraph("Pesanan status 'Batal'<br/>× Nilai Pesanan", style_td),
            Paragraph("Pesanan status 'Dibatalkan'<br/>× Nilai Pesanan", style_td),
            Paragraph("<font color='#e11d48'>Σ Transaksi Status Batal</font>", style_td_bold),
            Paragraph("Potensi omset transaksi yang gagal masuk kas akibat cancel.", style_td)
        ]
    ]

    t_fin = Table(table_fin_data, colWidths=[0.8*cm, 3.2*cm, 3.6*cm, 3.6*cm, 3.8*cm, 3.0*cm])
    t_fin.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#ffffff")),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor("#fff1f2")),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor("#f0fdf4")),
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor("#eef2ff")),
        ('BACKGROUND', (0,5), (-1,5), colors.HexColor("#eff6ff")),
        ('BACKGROUND', (0,6), (-1,6), colors.HexColor("#fff1f2")),
    ]))
    story.append(t_fin)
    story.append(Spacer(1, 10))

    # 4. PENJELASAN KHUSUS TOTAL DISKON & KOMPONEN POTONGAN
    story.append(Paragraph("2. PENJELASAN MENDALAM: ASAL-USUL TOTAL DISKON & KOMPONEN POTONGAN", style_h2))
    
    diskon_detail_p1 = (
        "Pertanyaan yang kerap muncul adalah: <i>'Di mana rincian kolom potongan-potongan dan bagaimana Total Diskon dihitung?'</i><br/>"
        "Di platform marketplace, diskon bukan hanya satu macam, melainkan gabungan dari beberapa pos potongan:"
    )
    story.append(Paragraph(diskon_detail_p1, style_body))

    diskon_breakdown_data = [
        [
            Paragraph("<b>Platform</b>", style_table_header),
            Paragraph("<b>Kolom Mentah Asli di Excel Marketplace</b>", style_table_header),
            Paragraph("<b>Logika Sistem & Alasan Perhitungan</b>", style_table_header)
        ],
        [
            Paragraph("<b>TIKTOK SHOP</b>", style_td_bold),
            Paragraph(
                "• <b>SKU Platform Discount</b> (Col 15)<br/>"
                "• <b>SKU Seller Discount</b> (Col 16)",
                style_td
            ),
            Paragraph(
                "TikTok secara eksplisit memisahkan diskon subsidi platform dan diskon voucher toko. "
                "Sistem FTL menjumlahkan keduanya: <b>Platform Discount + Seller Discount</b> sehingga "
                "tercatat utuh pada kolom <b>Total Diskon</b>.",
                style_td
            )
        ],
        [
            Paragraph("<b>SHOPEE</b>", style_td_bold),
            Paragraph(
                "• <b>Subtotal Pesanan</b> (Col 24)<br/>"
                "• <b>Total Pembayaran</b> (Col 42)<br/>"
                "• <i>(Kolom bawaan Shopee: Total Diskon - Col 25)</i>",
                style_td
            ),
            Paragraph(
                "<b>Mengapa tidak memakai kolom bawaan 'Total Diskon' Shopee?</b><br/>"
                "Kolom bawaan Shopee menghitung diskon dari <i>harga coret katalog</i> awal yang sangat tinggi. "
                "Jika angka tersebut dijumlahkan, total diskon menjadi tidak realistis dan sering kali melebihi "
                "harga asli produk. Oleh karena itu, sistem FTL menggunakan rumus <b>Diskon Riil Toko</b>:<br/>"
                "<b>Total Diskon Riil = Subtotal Pesanan − Total Pembayaran</b>.<br/>"
                "Rumus ini 100% akurat merefleksikan selisih harga jual toko terhadap uang yang benar-benar dibayarkan pembeli.",
                style_td
            )
        ]
    ]

    t_diskon = Table(diskon_breakdown_data, colWidths=[2.8*cm, 6.0*cm, 9.2*cm])
    t_diskon.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#f8fafc")),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor("#ffffff")),
    ]))
    story.append(t_diskon)
    story.append(Spacer(1, 10))

    # 5. DIAGRAM LOGIKA RUMUS MATEMATIKA
    story.append(Paragraph("3. ALUR LOGIKA RUMUS & PERSAMAAN MATEMATIKA", style_h2))
    
    formula_box_data = [
        [
            Paragraph("<b>1. ALUR PENDAPATAN BERSIH:</b>", ParagraphStyle('FHead1', fontName='Helvetica-Bold', fontSize=8, textColor=c_emerald)),
            Paragraph("<b>2. ALUR MODAL POKOK (HPP):</b>", ParagraphStyle('FHead2', fontName='Helvetica-Bold', fontSize=8, textColor=c_indigo)),
            Paragraph("<b>3. ALUR ESTIMASI LABA:</b>", ParagraphStyle('FHead3', fontName='Helvetica-Bold', fontSize=8, textColor=c_blue))
        ],
        [
            Paragraph(
                "<font color='#0f172a'><b>OMSET KOTOR</b></font><br/>"
                "<font color='#e11d48'>− Total Diskon (Voucher/Promo)</font><br/>"
                "<b>= OMSET BERSIH</b><br/>"
                "<font size=7 color='#64748b'><i>(Uang riil yang dibayar pembeli)</i></font>",
                style_td
            ),
            Paragraph(
                "<font color='#0f172a'><b>QTY PESANAN SELESAI</b></font><br/>"
                "<font color='#4f46e5'>× HPP Satuan (@Rp 25.000)</font><br/>"
                "<b>= TOTAL HPP</b><br/>"
                "<font size=7 color='#64748b'><i>(Pesanan batal tidak dihitung HPP)</i></font>",
                style_td
            ),
            Paragraph(
                "<font color='#059669'><b>OMSET BERSIH</b></font><br/>"
                "<font color='#4f46e5'>− Total HPP (Modal Barang)</font><br/>"
                "<b>= ESTIMASI LABA BERSIH</b><br/>"
                "<font size=7 color='#64748b'><i>(Profit kotor sebelum operational overhead)</i></font>",
                style_td
            )
        ]
    ]

    t_box = Table(formula_box_data, colWidths=[6.0*cm, 6.0*cm, 6.0*cm])
    t_box.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#f0fdf4")),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#eef2ff")),
        ('BACKGROUND', (2,0), (2,0), colors.HexColor("#eff6ff")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_box)
    story.append(Spacer(1, 10))

    # 6. SIMULASI PERHITUNGAN TRANSAKSI RIIL (STUDI KASUS)
    story.append(Paragraph("4. SIMULASI CONTOH TRANSAKSI RIIL DARI LAPORAN EXCEL", style_h2))
    
    sim_data = [
        [
            Paragraph("<b>Studi Kasus</b>", style_table_header),
            Paragraph("<b>Data Kolom Asli File Excel</b>", style_table_header),
            Paragraph("<b>Hasil Olahan Sistem FTL</b>", style_table_header),
            Paragraph("<b>Keterangan Perhitungan</b>", style_table_header)
        ],
        [
            Paragraph("<b>Contoh 1:<br/>Shopee</b><br/>(3 pcs Calming Rub)", style_td),
            Paragraph(
                "• Subtotal Pesanan: <b>Rp 353.997</b><br/>"
                "• Total Pembayaran: <b>Rp 147.138</b><br/>"
                "• Status: <b>Selesai</b> (Qty: 3)",
                style_td
            ),
            Paragraph(
                "• Omset Kotor: <b>Rp 353.997</b><br/>"
                "• Diskon: <font color='#e11d48'><b>Rp 206.859</b></font><br/>"
                "• Omset Bersih: <font color='#059669'><b>Rp 147.138</b></font><br/>"
                "• Total HPP: <font color='#4f46e5'><b>Rp 75.000</b></font><br/>"
                "• Laba: <font color='#2563eb'><b>Rp 72.138</b></font>",
                style_td
            ),
            Paragraph(
                "Diskon dihitung dari selisih Rp 353.997 − Rp 147.138 = Rp 206.859.<br/>"
                "HPP dihitung 3 pcs × Rp 25.000 = Rp 75.000.<br/>"
                "Laba dihitung Rp 147.138 − Rp 75.000 = <b>Rp 72.138</b>.",
                style_td
            )
        ],
        [
            Paragraph("<b>Contoh 2:<br/>TikTok Shop</b><br/>(1 pcs Calming Rub)", style_td),
            Paragraph(
                "• Subtotal Before Disc: <b>Rp 299.999</b><br/>"
                "• Platform Disc: <b>Rp 200.000</b><br/>"
                "• Seller Disc: <b>Rp 43.562</b><br/>"
                "• Order Amount: <b>Rp 56.437</b><br/>"
                "• Status: <b>Selesai</b> (Qty: 1)",
                style_td
            ),
            Paragraph(
                "• Omset Kotor: <b>Rp 299.999</b><br/>"
                "• Diskon: <font color='#e11d48'><b>Rp 243.562</b></font><br/>"
                "• Omset Bersih: <font color='#059669'><b>Rp 56.437</b></font><br/>"
                "• Total HPP: <font color='#4f46e5'><b>Rp 25.000</b></font><br/>"
                "• Laba: <font color='#2563eb'><b>Rp 31.437</b></font>",
                style_td
            ),
            Paragraph(
                "Diskon dihitung dari Col 15 + Col 16 = Rp 200rb + Rp 43.562 = Rp 243.562.<br/>"
                "Omset Bersih sesuai uang masuk Col 30 = Rp 56.437.<br/>"
                "HPP 1 pcs × Rp 25.000 = Rp 25.000.<br/>"
                "Laba dihitung Rp 56.437 − Rp 25.000 = <b>Rp 31.437</b>.",
                style_td
            )
        ]
    ]

    t_sim = Table(sim_data, colWidths=[2.8*cm, 5.0*cm, 4.2*cm, 6.0*cm])
    t_sim.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#f8fafc")),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor("#ffffff")),
    ]))
    story.append(t_sim)
    story.append(Spacer(1, 10))

    # 7. CARA MELIHAT PAPAN KALKULASI DI WEBSITE
    story.append(Paragraph("5. CARA MENGECEK & MENGATUR HPP DI WEBSITE LAPORAN", style_h2))
    
    web_guide = (
        "1. Buka website <b>https://laporanftl.vercel.app</b> dan upload file laporan Shopee / TikTok.<br/>"
        "2. Pada <b>Sidebar Menu Sebelah Kiri</b>, klik menu <b>'Keuangan & Laba'</b>.<br/>"
        "3. Anda akan melihat <b>6 Kartu Finansial Besar</b> beserta <b>Papan Rincian Kalkulasi Nominal</b> interaktif "
        "yang menunjukkan rumus secara langsung dengan angka riil dari file yang diupload.<br/>"
        "4. <b>Pengaturan Nilai Modal HPP:</b> Jika ada perubahan harga pokok per pcs (misal dari Rp 25.000 menjadi Rp 26.000), "
        "cukup ubah angka pada kotak <i>'Pengaturan HPP Satuan per Pcs'</i>. Seluruh angka Total HPP dan Estimasi Laba "
        "di tabel dan ekspor Excel akan langsung terhitung ulang secara otomatis."
    )
    story.append(Paragraph(web_guide, style_body))
    story.append(Spacer(1, 12))

    # SIGN-OFF BLOCK
    signoff_text = (
        "<b>Catatan Finansial Internal:</b> Seluruh perhitungan ini dirancang untuk memberikan transparansi penuh "
        "terhadap arus kas masuk, modal produk keluar, dan efisiensi promosi voucher toko For The Little. "
        "Dokumen ini berlaku sebagai acuan standar tim operasional dan keuangan FTL."
    )
    signoff_table = Table([[Paragraph(signoff_text, style_callout)]], colWidths=[18.0*cm])
    signoff_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#e9f1ec")),
        ('BOX', (0,0), (-1,-1), 1, c_sage),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(signoff_table)

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated: {filename}")

if __name__ == "__main__":
    output_pdf = r"c:\xamppnew\htdocs\laporan-FTL\Panduan_Rumus_Finansial_FTL.pdf"
    build_pdf(output_pdf)
    
    # Also copy to artifact directory
    artifact_dir = r"C:\Users\momo\.gemini\antigravity\brain\a480af5b-0056-4f46-9bb4-b8c6a2b7f7e1"
    if os.path.exists(artifact_dir):
        artifact_pdf = os.path.join(artifact_dir, "Panduan_Rumus_Finansial_FTL.pdf")
        shutil.copyfile(output_pdf, artifact_pdf)
        print(f"Copied to artifact directory: {artifact_pdf}")
