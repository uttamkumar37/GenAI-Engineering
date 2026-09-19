# 07 — Embeddings & Vector Databases — Fresher

**Concepts**: what an embedding is, embedding models (API-based vs local), similarity search basics, what a vector database does differently from a normal DB.

**Resources**:
- [OpenAI — Embeddings guide](https://platform.openai.com/docs/guides/embeddings)
- [Qdrant — What is a vector database](https://qdrant.tech/articles/what-is-a-vector-database/)

**Code** (`code/07-embeddings-vector-db/01-fresher/`):
- `generate_embeddings.py` — embed 10 sentences via API, compute pairwise cosine similarity, print closest pairs

**Interview questions**:
- Why can't you just use a SQL `LIKE` query instead of a vector DB for semantic search? (Lexical match vs semantic/meaning match — no shared keywords doesn't mean unrelated meaning.)
