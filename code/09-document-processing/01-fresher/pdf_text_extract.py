# requires pymupdf and pypdf; run make_sample_pdf.py first to generate sample_data/sample_report.pdf
from __future__ import annotations

from pathlib import Path

import pymupdf
from pypdf import PdfReader

from make_sample_pdf import build_sample_pdf

SAMPLE_PDF = Path(__file__).parent / "sample_data" / "sample_report.pdf"


def extract_with_pymupdf(pdf_path: Path) -> list[str]:
    doc = pymupdf.open(pdf_path)
    return [page.get_text() for page in doc]


def extract_with_pypdf(pdf_path: Path) -> list[str]:
    reader = PdfReader(str(pdf_path))
    return [page.extract_text() or "" for page in reader.pages]


if __name__ == "__main__":
    if not SAMPLE_PDF.exists():
        build_sample_pdf(SAMPLE_PDF)

    pymupdf_pages = extract_with_pymupdf(SAMPLE_PDF)
    pypdf_pages = extract_with_pypdf(SAMPLE_PDF)

    for i, (a, b) in enumerate(zip(pymupdf_pages, pypdf_pages)):
        print(f"--- page {i + 1} ---")
        print(f"[pymupdf] {len(a)} chars:\n{a[:300]}\n")
        print(f"[pypdf]   {len(b)} chars:\n{b[:300]}\n")
