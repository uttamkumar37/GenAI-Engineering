# CrossEncoderReranker requires `sentence-transformers` (downloads a model on first use)
from __future__ import annotations

import hashlib
import os
from abc import ABC, abstractmethod

CORPUS = [
    "The Eiffel Tower is located in Paris, France.",
    "Paris is the capital city of France.",
    "The Great Wall of China stretches thousands of kilometers.",
    "France's economy is one of the largest in Europe.",
    "The Louvre museum in Paris houses the Mona Lisa.",
    "Berlin is the capital of Germany.",
    "The French Riviera is a popular tourist destination.",
    "Napoleon Bonaparte was a French military leader.",
    "The Seine river flows through Paris.",
    "Croissants are a traditional French pastry.",
] * 2  # pad past 10 to demonstrate retrieving a top-20 candidate set

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


def vector_search(query: str, top_k: int = 20) -> list[tuple[int, str, float]]:
    query_vec = fake_embed(query)
    scored = [(i, doc, cosine_similarity(query_vec, fake_embed(doc))) for i, doc in enumerate(CORPUS)]
    scored.sort(key=lambda t: t[2], reverse=True)
    return scored[:top_k]


class Reranker(ABC):
    @abstractmethod
    def score(self, query: str, documents: list[str]) -> list[float]: ...


class CrossEncoderReranker(Reranker):
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2") -> None:
        from sentence_transformers import CrossEncoder

        self.model = CrossEncoder(model_name)

    def score(self, query: str, documents: list[str]) -> list[float]:
        pairs = [(query, doc) for doc in documents]
        return list(self.model.predict(pairs))


class FakeReranker(Reranker):
    # deterministic lexical-overlap stand-in for a cross-encoder
    def score(self, query: str, documents: list[str]) -> list[float]:
        query_words = set(query.lower().split())
        scores = []
        for doc in documents:
            doc_words = set(doc.lower().split())
            overlap = len(query_words & doc_words)
            scores.append(overlap / (len(query_words) + 1))
        return scores


def rerank_pipeline(query: str, reranker: Reranker, top_k_retrieve: int = 20, top_k_final: int = 5):
    candidates = vector_search(query, top_k=top_k_retrieve)
    docs = [text for _, text, _ in candidates]
    rerank_scores = reranker.score(query, docs)
    reranked = sorted(zip(candidates, rerank_scores), key=lambda t: t[1], reverse=True)
    return candidates, reranked[:top_k_final]


if __name__ == "__main__":
    query = "Where is the Eiffel Tower and what else is in that city?"
    reranker: Reranker = (
        CrossEncoderReranker() if os.environ.get("USE_REAL_RERANKER") else FakeReranker()
    )
    before, after = rerank_pipeline(query, reranker)

    print("Before rerank (vector search order, top 5 of 20):")
    for i, (idx, doc, score) in enumerate(before[:5]):
        print(f"  {i}. ({score:.3f}) {doc}")

    print("\nAfter rerank (top 5):")
    for i, ((idx, doc, vec_score), rerank_score) in enumerate(after):
        print(f"  {i}. (rerank={rerank_score:.3f}, vector={vec_score:.3f}) {doc}")
