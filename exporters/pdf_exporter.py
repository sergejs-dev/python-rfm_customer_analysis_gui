from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def export_pdf(rfm_df, segment_counts, file_path):

    c = canvas.Canvas(file_path, pagesize=letter)

    width, height = letter
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "RFM Customer Analysis Report")

    y -= 40

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Customer Segments Summary")

    y -= 20
    c.setFont("Helvetica", 11)

    for segment, count in segment_counts.items():
        line = f"{segment}: {count}"
        c.drawString(60, y, line)
        y -= 18

    y -= 20

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Top Customers by Monetary Value")

    y -= 20
    c.setFont("Helvetica", 11)

    top_customers = rfm_df.sort_values(by="Monetary", ascending=False).head(5)

    for index, row in top_customers.iterrows():
        line = f"{index}  -  Revenue: {row['Monetary']}"
        c.drawString(60, y, line)
        y -= 18

    c.save()