# 09 — Document Processing — Advanced / Senior

**Concepts**: multimodal document understanding (vision-capable LLMs reading document images directly instead of OCR pipeline), speech-to-text integration (Whisper or provider APIs) for audio documents, combining multimodal extraction with RAG (image/chart understanding as retrievable context), handling messy real-world documents at scale (error recovery, partial-extraction fallbacks).

**Resources**:
- [Anthropic — Vision capabilities](https://docs.anthropic.com/en/docs/build-with-claude/vision)
- [OpenAI Whisper — GitHub](https://github.com/openai/whisper)

**Code** (`code/09-document-processing/03-advanced/`):
- `vision_llm_doc_understanding.py` — feed a complex table/chart-containing page image directly to a vision-capable model, compare answer quality vs OCR+text pipeline
- `multimodal_rag_pipeline.py` — RAG system that can retrieve and reason over both text chunks and document images

**Interview questions**:
- When would you use a vision-LLM directly on a document image instead of an OCR+parsing pipeline? (Complex layouts, charts, mixed content where OCR loses structure — tradeoff is cost/latency per page vs accuracy.)
