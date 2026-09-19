from __future__ import annotations

import math
from dataclasses import dataclass


class FakeEmbedder:
    """Deterministic bag-of-words embedder (no network/model call) — stands in for a real
    embeddings API so cache-key/similarity logic is genuinely exercised end to end."""

    def embed(self, text: str) -> dict[str, float]:
        words = [w.strip(".,!?").lower() for w in text.split()]
        vec: dict[str, float] = {}
        for w in words:
            vec[w] = vec.get(w, 0.0) + 1.0
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
        return {k: v / norm for k, v in vec.items()}


def cosine_similarity(a: dict[str, float], b: dict[str, float]) -> float:
    shared_keys = set(a) & set(b)
    return sum(a[k] * b[k] for k in shared_keys)


@dataclass
class CacheEntry:
    prompt: str
    embedding: dict[str, float]
    response: str


class SemanticCache:
    def __init__(self, embedder: FakeEmbedder, similarity_threshold: float = 0.8) -> None:
        self._embedder = embedder
        self._threshold = similarity_threshold
        self._entries: list[CacheEntry] = []
        self.hits = 0
        self.misses = 0

    def get(self, prompt: str) -> tuple[str | None, float]:
        query_vec = self._embedder.embed(prompt)
        best_score = 0.0
        best_entry: CacheEntry | None = None
        for entry in self._entries:
            score = cosine_similarity(query_vec, entry.embedding)
            if score > best_score:
                best_score = score
                best_entry = entry

        if best_entry is not None and best_score >= self._threshold:
            self.hits += 1
            return best_entry.response, best_score

        self.misses += 1
        return None, best_score

    def set(self, prompt: str, response: str) -> None:
        self._entries.append(CacheEntry(prompt=prompt, embedding=self._embedder.embed(prompt), response=response))


class FakeLLM:
    def complete(self, prompt: str) -> str:
        return f"Answer to: {prompt}"


def cached_complete(cache: SemanticCache, llm: FakeLLM, prompt: str) -> tuple[str, bool, float]:
    cached_response, score = cache.get(prompt)
    if cached_response is not None:
        return cached_response, True, score

    response = llm.complete(prompt)
    cache.set(prompt, response)
    return response, False, score


if __name__ == "__main__":
    embedder = FakeEmbedder()
    cache = SemanticCache(embedder, similarity_threshold=0.6)
    llm = FakeLLM()

    prompts = [
        "What is the refund policy?",
        "What's your refund policy?",  # near-duplicate, should hit cache
        "Tell me the weather forecast for today",  # unrelated, should miss
        "What is the refund policy for orders?",  # similar enough, should hit
    ]

    for prompt in prompts:
        response, was_hit, score = cached_complete(cache, llm, prompt)
        status = "HIT" if was_hit else "MISS"
        print(f"[{status:4s}] score={score:.2f}  prompt={prompt!r} -> {response}")

    print(f"\nCache stats: {cache.hits} hits, {cache.misses} misses")
    print(
        "\nRisk of an aggressive threshold: a lower similarity_threshold returns cached answers "
        "for queries that are similar in wording but require a different answer (e.g. 'refund "
        "policy for orders' vs 'refund policy for subscriptions') — tune the threshold against "
        "real query pairs, not just eyeballing similarity scores."
    )
