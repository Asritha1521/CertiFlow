
from pathlib import Path
from uuid import uuid4

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


OUTPUT_DIR = Path("generated")


def generate_certificate(
    recipient_name: str,
    event_name: str,
    certificate_id: int
) -> str:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    filename = f"certificate_{certificate_id}_{uuid4().hex[:8]}.pdf"
    file_path = OUTPUT_DIR / filename

    page_width, page_height = landscape(A4)
    pdf = canvas.Canvas(str(file_path), pagesize=(page_width, page_height))

    # Certificate border
    pdf.setStrokeColor(colors.HexColor("#174A7E"))
    pdf.setLineWidth(4)
    pdf.rect(1 * cm, 1 * cm, page_width - 2 * cm, page_height - 2 * cm)

    # Certificate title
    pdf.setFillColor(colors.HexColor("#174A7E"))
    pdf.setFont("Helvetica-Bold", 30)
    pdf.drawCentredString(
        page_width / 2,
        page_height - 4 * cm,
        "CERTIFICATE OF PARTICIPATION"
    )

    # Recipient name
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica", 17)
    pdf.drawCentredString(
        page_width / 2,
        page_height - 6 * cm,
        "This certificate is proudly presented to"
    )

    pdf.setFillColor(colors.HexColor("#B8860B"))
    pdf.setFont("Helvetica-Bold", 27)
    pdf.drawCentredString(
        page_width / 2,
        page_height - 8 * cm,
        recipient_name
    )

    # Event details
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(
        page_width / 2,
        page_height - 10 * cm,
        f"For participating in {event_name}"
    )

    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(
        page_width / 2,
        2.5 * cm,
        f"Certificate ID: {certificate_id}"
    )

    pdf.save()
    return str(file_path)
