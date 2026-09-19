# 09 — Document Processing — Intermediate

**Concepts**: table extraction (structure-aware parsing), OCR for scanned documents (Tesseract or cloud OCR), layout-aware parsing (headers, sections), handling multi-column PDFs, image extraction from documents.

**Resources**:
- [unstructured.io — docs](https://docs.unstructured.io/welcome)
- [Tesseract OCR — docs](https://tesseract-ocr.github.io/tessdoc/)

**Code** (`code/09-document-processing/02-intermediate/`):
- `table_extraction.py` — extract tables from a PDF into structured DataFrames
- `ocr_scanned_doc.py` — run OCR on a scanned/image-based PDF, clean up output

**Interview questions**:
- How would you build a document ingestion pipeline that handles both digital and scanned PDFs reliably? (Detect text layer presence first; fall back to OCR; validate extraction confidence before indexing.)
