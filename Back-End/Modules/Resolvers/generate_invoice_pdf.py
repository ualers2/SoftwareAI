from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import json

def generate_invoice_pdf(invoice, output_dir="../../Invoices"):
    pdf_filename = f"invoice_{invoice.id}.pdf"
    pdf_path = os.path.join(output_dir, pdf_filename)

    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "INVOICE")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Invoice Number: {invoice.number}")
    c.drawString(50, height - 120, f"Date: {invoice.date.strftime('%Y-%m-%d')}")
    c.drawString(50, height - 140, f"User ID: {invoice.user_id}")
    c.drawString(50, height - 160, f"Plan: {invoice.plan_name}")

    c.drawString(50, height - 200, "Items:")
    y = height - 220
    lines = json.loads(invoice.lines) if invoice.lines else []
    for line in lines:
        c.drawString(60, y, f"{line['description']} x {line['qty']} - ${line['price']:.2f}")
        y -= 20

    c.drawString(50, y - 20, f"Total Amount: ${float(invoice.amount):.2f} {invoice.currency}")

    c.showPage()
    c.save()
    print(f"pdf_path {pdf_path}")
    return pdf_path
