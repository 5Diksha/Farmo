from pathlib import Path

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

PDF_DIR = Path("exports")
PDF_DIR.mkdir(exist_ok=True)


def create_invoice_pdf(
    customer_name,
    month_name,
    year,
    summary
):

    file_name = (
        f"{customer_name}_{month_name}_{year}.pdf"
    )

    file_path = PDF_DIR / file_name

    doc = SimpleDocTemplate(str(file_path))

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "GOLE TRACTOR SERVICES",
            styles["Title"]
        )
    )

    content.append(
        Paragraph(
            "Owner: Dipak Gole",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            "Powered by Farmo",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            "FARMO INVOICE",
            styles["Heading1"]
        )
    )

    content.append(
        Paragraph(
            f"Customer: {customer_name}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Month: {month_name} {year}",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            "<b>WORK SUMMARY</b>",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            f"Rotavator: "
            f"{summary['rot_hours']:.2f} Hours "
            f" | ₹{summary['rot_amount']:.2f}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Nangarat: "
            f"{summary['nangarat_hours']:.2f} Hours "
            f" | ₹{summary['nangarat_amount']:.2f}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Fanadi: "
            f"{summary['fanadi_hours']:.2f} Hours "
            f" | ₹{summary['fanadi_amount']:.2f}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Trolley Trip: "
            f"{summary['trolley_trips']} Trips "
            f" | ₹{summary['trolley_amount']:.2f}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Water Tanker Trip: "
            f"{summary['tanker_trips']} Trips "
            f" | ₹{summary['tanker_amount']:.2f}",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            f"Total Work Amount: ₹{summary['total_work_amount']:.2f}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Advance Received: ₹{summary['total_credit']:.2f}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Payments Received: ₹{summary['total_payments']:.2f}",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            f"<b>PENDING BALANCE: ₹{summary['balance']:.2f}</b>",
            styles["Heading2"]
        )
    )

    doc.build(content)

    return file_path