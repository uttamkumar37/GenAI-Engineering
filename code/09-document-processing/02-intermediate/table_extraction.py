# requires pdfplumber and pandas; uses the sample PDF from ../01-fresher/sample_data
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pdfplumber

SAMPLE_PDF = Path(__file__).parent.parent / "01-fresher" / "sample_data" / "sample_report.pdf"


def extract_tables(pdf_path: Path) -> list[pd.DataFrame]:
    frames = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                if not table or len(table) < 2:
                    continue
                header, *rows = table
                frames.append(pd.DataFrame(rows, columns=header))
    return frames


if __name__ == "__main__":
    if not SAMPLE_PDF.exists():
        sys.path.insert(0, str(SAMPLE_PDF.parent.parent))
        from make_sample_pdf import build_sample_pdf

        build_sample_pdf(SAMPLE_PDF)

    tables = extract_tables(SAMPLE_PDF)
    print(f"Found {len(tables)} table(s)")
    for i, df in enumerate(tables):
        print(f"\n--- table {i + 1} ---")
        print(df.to_string(index=False))
