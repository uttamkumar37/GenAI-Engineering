# requires reportlab
from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

SAMPLE_DIR = Path(__file__).parent / "sample_data"
OUTPUT_PATH = SAMPLE_DIR / "sample_report.pdf"

TABLE_DATA = [
    ["Quarter", "Revenue ($M)", "Costs ($M)", "Net Margin"],
    ["Q1 2026", "4.2", "3.1", "26%"],
    ["Q2 2026", "4.8", "3.6", "25%"],
    ["Q3 2026", "5.1", "3.7", "27%"],
]


def build_sample_pdf(output_path: Path = OUTPUT_PATH) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(str(output_path), pagesize=letter)
    story = [
        Paragraph("Acme Corp — Quarterly Report", styles["Title"]),
        Spacer(1, 0.2 * inch),
        Paragraph(
            "This is a synthetically generated sample document used to exercise PDF "
            "text and table extraction code. Page 1 contains narrative text; page 2 "
            "contains a structured financial table.",
            styles["BodyText"],
        ),
        Spacer(1, 0.3 * inch),
        Paragraph(
            "Revenue grew steadily across the year, driven by new enterprise contracts "
            "and expansion into adjacent markets. Operating costs also rose, primarily "
            "due to increased cloud infrastructure spend.",
            styles["BodyText"],
        ),
    ]
    story.append(Spacer(1, 1 * inch))
    story.append(Paragraph("Financial Summary", styles["Heading2"]))
    table = Table(TABLE_DATA, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#333333")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f0f0")]),
            ]
        )
    )
    story.append(table)
    doc.build(story)
    return output_path


if __name__ == "__main__":
    path = build_sample_pdf()
    print(f"Wrote sample PDF to {path}")
