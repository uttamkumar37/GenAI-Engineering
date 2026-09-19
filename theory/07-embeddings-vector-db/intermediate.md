# 07 — Embeddings & Vector Databases — Intermediate

**Concepts**: chunking strategies (fixed-size, recursive, semantic chunking), metadata filtering, indexing (HNSW basics conceptually), pgvector setup, Qdrant setup (collections, payloads, filters).

**Resources**:
- [pgvector — GitHub README](https://github.com/pgvector/pgvector)
- [Qdrant — Quickstart](https://qdrant.tech/documentation/quickstart/)
- LangChain — Text Splitters overview (verify current API surface — churns often)

**Code** (`code/07-embeddings-vector-db/02-intermediate/`):
- `chunking_strategies_compare.py` — same document, 3 chunking methods, compare resulting chunk counts/coherence
- `pgvector_ingest_search/` — ingest chunked docs with embeddings into Postgres+pgvector, run similarity search with metadata filter (e.g. filter by document date)

**Interview questions**:
- How does chunk size affect both retrieval quality and generation quality downstream? (Too small loses context; too large dilutes relevance and wastes context window.)
