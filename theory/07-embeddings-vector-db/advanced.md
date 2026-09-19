# 07 — Embeddings & Vector Databases — Advanced / Senior

**Concepts**: hybrid search (dense + sparse/BM25 combined), reranking models (cross-encoders), embedding model selection tradeoffs (dimensionality, cost, domain fit, fine-tuned embeddings), handling embedding drift when swapping models, scaling vector search (sharding/index tuning conceptually), metadata schema design for filterable multi-tenant RAG.

**Resources**:
- [Qdrant — Hybrid Search](https://qdrant.tech/documentation/concepts/hybrid-queries/)
- [SBERT — Cross-Encoders for reranking](https://www.sbert.net/examples/applications/cross-encoder/README.html)

**Code** (`code/07-embeddings-vector-db/03-advanced/`):
- `hybrid_search_bm25_dense.py` — combine BM25 keyword scores with dense vector scores, reciprocal rank fusion
- `reranker_pipeline.py` — retrieve top-20 with vector search, rerank to top-5 with a cross-encoder, compare ordering before/after

**Interview questions**:
- Your RAG system retrieves relevant-looking but ultimately unhelpful chunks. Is this a chunking, embedding, or retrieval-ranking problem — how do you diagnose? (Systematic diagnosis: eyeball retrieved chunks first, check chunk boundaries, then test hybrid+rerank before touching the embedding model.)
