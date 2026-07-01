from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from pathlib import Path


def export_pdf(text: str, output_path: str):
    """
    Markdown文本 → PDF
    """

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    c = canvas.Canvas(str(path), pagesize=A4)

    width, height = A4
    y = height - 40

    for line in text.split("\n"):
        if y < 40:
            c.showPage()
            y = height - 40

        c.drawString(40, y, line[:110])  # 防止过长
        y -= 15

    c.save()

    return str(path)