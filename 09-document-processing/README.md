# 09 — Document Processing

## Fresher

**Concepts**: extracting text from PDFs, basic OCR concept, handling different file types (txt, docx, pdf, html).

**Resources**:
- [PyMuPDF (fitz) — quickstart](https://pymupdf.readthedocs.io/en/latest/tutorial.html)

**Code** (`code/01-fresher/`):
- `pdf_text_extract.py` — extract raw text from a few sample PDFs, compare quality across libraries (PyMuPDF vs pypdf)

**Interview questions**:
- Why does naive PDF text extraction often break table structure? (PDFs store positioned text/glyphs, not semantic structure — tables are visual layout, not tagged data.)

## Intermediate

**Concepts**: table extraction (structure-aware parsing), OCR for scanned documents (Tesseract or cloud OCR), layout-aware parsing (headers, sections), handling multi-column PDFs, image extraction from documents.

**Resources**:
- [unstructured.io — docs](https://docs.unstructured.io/welcome)
- [Tesseract OCR — docs](https://tesseract-ocr.github.io/tessdoc/)

**Code** (`code/02-intermediate/`):
- `table_extraction.py` — extract tables from a PDF into structured DataFrames
- `ocr_scanned_doc.py` — run OCR on a scanned/image-based PDF, clean up output

**Interview questions**:
- How would you build a document ingestion pipeline that handles both digital and scanned PDFs reliably? (Detect text layer presence first; fall back to OCR; validate extraction confidence before indexing.)

## Advanced / Senior

**Concepts**: multimodal document understanding (vision-capable LLMs reading document images directly instead of OCR pipeline), speech-to-text integration (Whisper or provider APIs) for audio documents, combining multimodal extraction with RAG (image/chart understanding as retrievable context), handling messy real-world documents at scale (error recovery, partial-extraction fallbacks).

**Resources**:
- [Anthropic — Vision capabilities](https://docs.anthropic.com/en/docs/build-with-claude/vision)
- [OpenAI Whisper — GitHub](https://github.com/openai/whisper)

**Code** (`code/03-advanced/`):
- `vision_llm_doc_understanding.py` — feed a complex table/chart-containing page image directly to a vision-capable model, compare answer quality vs OCR+text pipeline
- `multimodal_rag_pipeline.py` — RAG system that can retrieve and reason over both text chunks and document images

**Interview questions**:
- When would you use a vision-LLM directly on a document image instead of an OCR+parsing pipeline? (Complex layouts, charts, mixed content where OCR loses structure — tradeoff is cost/latency per page vs accuracy.)

## Milestone

Feed a real messy PDF (multi-column, tables, a chart) through both an OCR-pipeline and a vision-LLM approach, document the accuracy/cost/latency comparison in this README — strong interview talking point.
