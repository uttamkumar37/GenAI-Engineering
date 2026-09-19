# requires ANTHROPIC_API_KEY for generation; embeddings use a deterministic fake client (swap in a real one for production)
from __future__ import annotations

import hashlib
import os

import anthropic

MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-opus-5")
EMBEDDING_DIM = 16

DOCUMENTS = [
    "The company's return policy allows returns within 30 days of purchase with a receipt.",
    "Shipping typically takes 3-5 business days for standard orders within the country.",
    "Our premium plan includes priority support and unlimited storage for $19.99/month.",
    "To reset your password, click 'Forgot password' on the login page and check your email.",
    "The warranty covers manufacturing defects for one year from the date of purchase.",
]


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


def retrieve(query: str, documents: list[str], top_k: int = 3) -> list[str]:
    query_vec = fake_embed(query)
    scored = [(cosine_similarity(query_vec, fake_embed(doc)), doc) for doc in documents]
    scored.sort(key=lambda t: t[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]


def generate_answer(client: anthropic.Anthropic, query: str, context_chunks: list[str]) -> str:
    context = "\n".join(f"- {c}" for c in context_chunks)
    prompt = (
        f"Answer the question using only the context below. If the context "
        f"doesn't contain the answer, say so.\n\nContext:\n{context}\n\nQuestion: {query}"
    )
    response = client.messages.create(
        model=MODEL, max_tokens=300, messages=[{"role": "user", "content": prompt}]
    )
    return next(b.text for b in response.content if b.type == "text")


def basic_rag(client: anthropic.Anthropic, query: str) -> str:
    chunks = retrieve(query, DOCUMENTS)
    return generate_answer(client, query, chunks)


if __name__ == "__main__":
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    print(basic_rag(client, "How long is the warranty?"))
