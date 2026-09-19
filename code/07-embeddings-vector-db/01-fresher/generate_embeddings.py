# requires OPENAI_API_KEY (uses OpenAI's embedding API; Anthropic has no first-party embeddings endpoint)
from __future__ import annotations

import itertools
import os

from openai import OpenAI

MODEL = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

SENTENCES = [
    "The cat sat on the mat.",
    "A feline rested on the rug.",
    "The stock market fell sharply today.",
    "Equities dropped significantly this afternoon.",
    "I love hiking in the mountains.",
    "Climbing peaks is one of my favorite hobbies.",
    "The recipe calls for two cups of flour.",
    "Bake the bread at 220 degrees.",
    "Quantum computers use qubits instead of bits.",
    "Photosynthesis converts sunlight into chemical energy.",
]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0


def embed_sentences(client: OpenAI, sentences: list[str]) -> list[list[float]]:
    response = client.embeddings.create(model=MODEL, input=sentences)
    return [item.embedding for item in response.data]


if __name__ == "__main__":
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    vectors = embed_sentences(client, SENTENCES)
    pairs = []
    for i, j in itertools.combinations(range(len(SENTENCES)), 2):
        sim = cosine_similarity(vectors[i], vectors[j])
        pairs.append((sim, SENTENCES[i], SENTENCES[j]))
    pairs.sort(reverse=True)
    print("Top 3 closest pairs:")
    for sim, a, b in pairs[:3]:
        print(f"  {sim:.4f}  {a!r}  <->  {b!r}")
