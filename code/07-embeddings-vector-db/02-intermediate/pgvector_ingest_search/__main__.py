from __future__ import annotations

import os

from .embeddings import EmbeddingClient, FakeEmbeddingClient, OpenAIEmbeddingClient
from .store import InMemoryVectorStore, PgVectorStore, VectorStore

DOCS = [
    ("d1", "Quarterly revenue grew 12% driven by cloud subscriptions.", {"doc_date": "2026-01-10"}),
    ("d2", "The new hiking trail offers panoramic mountain views.", {"doc_date": "2026-02-02"}),
    ("d3", "Cloud infrastructure costs were the main driver of margin pressure.", {"doc_date": "2026-03-15"}),
    ("d4", "A recipe for sourdough bread requires a live starter.", {"doc_date": "2026-01-20"}),
]


def build_store() -> VectorStore:
    dsn = os.environ.get("PGVECTOR_DSN")
    return PgVectorStore(dsn=dsn) if dsn else InMemoryVectorStore()


def build_embedding_client() -> EmbeddingClient:
    return OpenAIEmbeddingClient() if os.environ.get("OPENAI_API_KEY") else FakeEmbeddingClient()


def ingest(store: VectorStore, embedder: EmbeddingClient) -> None:
    ids, texts, metadatas = zip(*DOCS)
    vectors = embedder.embed(list(texts))
    store.upsert(list(ids), vectors, list(texts), list(metadatas))


def search(store: VectorStore, embedder: EmbeddingClient, query: str, doc_date: str | None = None):
    query_vector = embedder.embed([query])[0]
    metadata_filter = {"doc_date": doc_date} if doc_date else None
    return store.search(query_vector, top_k=3, metadata_filter=metadata_filter)


if __name__ == "__main__":
    embedder = build_embedding_client()
    store = build_store()
    ingest(store, embedder)

    print("Unfiltered search for 'cloud costs':")
    for result in search(store, embedder, "cloud costs"):
        print(f"  {result.score:.3f}  {result.doc_id}  {result.text}")

    print("\nFiltered to doc_date=2026-03-15:")
    for result in search(store, embedder, "cloud costs", doc_date="2026-03-15"):
        print(f"  {result.score:.3f}  {result.doc_id}  {result.text}")
