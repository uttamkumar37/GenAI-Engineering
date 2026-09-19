# 09 — Document Processing — Fresher

**Concepts**: extracting text from PDFs, basic OCR concept, handling different file types (txt, docx, pdf, html).

**Resources**:
- [PyMuPDF (fitz) — quickstart](https://pymupdf.readthedocs.io/en/latest/tutorial.html)

**Code** (`code/09-document-processing/01-fresher/`):
- `pdf_text_extract.py` — extract raw text from a few sample PDFs, compare quality across libraries (PyMuPDF vs pypdf)

**Interview questions**:
- Why does naive PDF text extraction often break table structure? (PDFs store positioned text/glyphs, not semantic structure — tables are visual layout, not tagged data.)
