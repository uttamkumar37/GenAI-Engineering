# requires the `rank-bm25` package; dense vectors use a deterministic fake embedding (swap in a real client for production)
from __future__ import annotations

import hashlib
from dataclasses import dataclass

from rank_bm25 import BM25Okapi

CORPUS = [
    "Retrieval-augmented generation grounds LLM answers in retrieved documents.",
    "BM25 is a classic sparse lexical ranking function based on term frequency.",
    "Dense retrieval uses embedding vectors and cosine similarity for semantic search.",
    "Hybrid search combines sparse lexical scores with dense vector scores.",
    "Reciprocal rank fusion merges multiple ranked lists into one ranking.",
    "Cross-encoder rerankers score a query-document pair jointly for higher precision.",
]

EMBEDDING_DIM = 16


def fake_embed(text: str) -> list[float]:
    return [
        (hashlib.sha256(f"{text}:{i}".encode()).digest()[0] / 255.0) * 2 - 1
        for i in range(EMBEDDING_DIM)
    ]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0


@dataclass
class RankedDoc:
    index: int
    text: str
    score: float


def bm25_rank(query: str) -> list[RankedDoc]:
    tokenized_corpus = [doc.lower().split() for doc in CORPUS]
    bm25 = BM25Okapi(tokenized_corpus)
    scores = bm25.get_scores(query.lower().split())
    ranked = sorted(enumerate(scores), key=lambda kv: kv[1], reverse=True)
    return [RankedDoc(i, CORPUS[i], score) for i, score in ranked]


def dense_rank(query: str) -> list[RankedDoc]:
    query_vec = fake_embed(query)
    scored = [(i, cosine_similarity(query_vec, fake_embed(doc))) for i, doc in enumerate(CORPUS)]
    scored.sort(key=lambda kv: kv[1], reverse=True)
    return [RankedDoc(i, CORPUS[i], score) for i, score in scored]


def reciprocal_rank_fusion(
    rankings: list[list[RankedDoc]], k: int = 60
) -> list[RankedDoc]:
    fused_scores: dict[int, float] = {}
    for ranking in rankings:
        for rank, doc in enumerate(ranking):
            fused_scores[doc.index] = fused_scores.get(doc.index, 0.0) + 1.0 / (k + rank + 1)
    ordered = sorted(fused_scores.items(), key=lambda kv: kv[1], reverse=True)
    return [RankedDoc(i, CORPUS[i], score) for i, score in ordered]


if __name__ == "__main__":
    query = "how does hybrid retrieval combine ranking signals"
    bm25_results = bm25_rank(query)
    dense_results = dense_rank(query)
    fused = reciprocal_rank_fusion([bm25_results, dense_results])

    print("BM25 ranking:")
    for doc in bm25_results[:3]:
        print(f"  {doc.score:.3f}  {doc.text}")
    print("\nDense ranking:")
    for doc in dense_results[:3]:
        print(f"  {doc.score:.3f}  {doc.text}")
    print("\nFused (RRF) ranking:")
    for doc in fused[:3]:
        print(f"  {doc.score:.4f}  {doc.text}")
