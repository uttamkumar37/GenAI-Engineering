# 07 — Embeddings & Vector Databases

## Fresher

**Concepts**: what an embedding is, embedding models (API-based vs local), similarity search basics, what a vector database does differently from a normal DB.

**Resources**:
- [OpenAI — Embeddings guide](https://platform.openai.com/docs/guides/embeddings)
- [Qdrant — What is a vector database](https://qdrant.tech/articles/what-is-a-vector-database/)

**Code** (`code/01-fresher/`):
- `generate_embeddings.py` — embed 10 sentences via API, compute pairwise cosine similarity, print closest pairs

**Interview questions**:
- Why can't you just use a SQL `LIKE` query instead of a vector DB for semantic search? (Lexical match vs semantic/meaning match — no shared keywords doesn't mean unrelated meaning.)

## Intermediate

**Concepts**: chunking strategies (fixed-size, recursive, semantic chunking), metadata filtering, indexing (HNSW basics conceptually), pgvector setup, Qdrant setup (collections, payloads, filters).

**Resources**:
- [pgvector — GitHub README](https://github.com/pgvector/pgvector)
- [Qdrant — Quickstart](https://qdrant.tech/documentation/quickstart/)
- LangChain — Text Splitters overview (verify current API surface — churns often)

**Code** (`code/02-intermediate/`):
- `chunking_strategies_compare.py` — same document, 3 chunking methods, compare resulting chunk counts/coherence
- `pgvector_ingest_search/` — ingest chunked docs with embeddings into Postgres+pgvector, run similarity search with metadata filter (e.g. filter by document date)

**Interview questions**:
- How does chunk size affect both retrieval quality and generation quality downstream? (Too small loses context; too large dilutes relevance and wastes context window.)

## Advanced / Senior

**Concepts**: hybrid search (dense + sparse/BM25 combined), reranking models (cross-encoders), embedding model selection tradeoffs (dimensionality, cost, domain fit, fine-tuned embeddings), handling embedding drift when swapping models, scaling vector search (sharding/index tuning conceptually), metadata schema design for filterable multi-tenant RAG.

**Resources**:
- [Qdrant — Hybrid Search](https://qdrant.tech/documentation/concepts/hybrid-queries/)
- [SBERT — Cross-Encoders for reranking](https://www.sbert.net/examples/applications/cross-encoder/README.html)

**Code** (`code/03-advanced/`):
- `hybrid_search_bm25_dense.py` — combine BM25 keyword scores with dense vector scores, reciprocal rank fusion
- `reranker_pipeline.py` — retrieve top-20 with vector search, rerank to top-5 with a cross-encoder, compare ordering before/after

**Interview questions**:
- Your RAG system retrieves relevant-looking but ultimately unhelpful chunks. Is this a chunking, embedding, or retrieval-ranking problem — how do you diagnose? (Systematic diagnosis: eyeball retrieved chunks first, check chunk boundaries, then test hybrid+rerank before touching the embedding model.)

## Milestone

A working hybrid-search + reranking pipeline over a real document set (e.g. your own resume + a few technical PDFs), queryable via a small API — this becomes a component of the capstone.
