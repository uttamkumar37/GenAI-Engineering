# 08 — RAG: Basic to Advanced — Fresher

**Concepts**: the basic RAG loop (retrieve → augment prompt → generate), why RAG reduces hallucination, simple single-collection RAG.

**Resources**:
- [Pinecone — What is Retrieval-Augmented Generation](https://www.pinecone.io/learn/retrieval-augmented-generation/)

**Code** (`code/08-rag-basic-to-advanced/01-fresher/`):
- `basic_rag_pipeline.py` — embed a small doc set, retrieve top-3 on a query, stuff into prompt, generate answer

**Interview questions**:
- Why does RAG reduce but not eliminate hallucination? (Model can still misread or overgeneralize from retrieved context, or retrieval itself can miss the right chunk.)
