# requires ANTHROPIC_API_KEY for AnthropicVerifierLLM; FakeVerifierLLM needs nothing
from __future__ import annotations

import hashlib
import json
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass

MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-opus-5")
EMBEDDING_DIM = 16

DOCUMENTS = [
    "The library is open from 9am to 6pm on weekdays.",
    "The library is closed on public holidays.",
    "Membership is free for local residents with proof of address.",
    "Overdue books incur a fine of $0.25 per day.",
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


def retrieve(query: str, top_k: int = 2) -> list[str]:
    query_vec = fake_embed(query)
    scored = [(cosine_similarity(query_vec, fake_embed(doc)), doc) for doc in DOCUMENTS]
    scored.sort(key=lambda t: t[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]


@dataclass
class VerificationResult:
    supported: bool
    unsupported_claims: list[str]


class VerifierLLM(ABC):
    @abstractmethod
    def generate(self, query: str, chunks: list[str]) -> str: ...

    @abstractmethod
    def verify(self, answer: str, chunks: list[str]) -> VerificationResult: ...


class AnthropicVerifierLLM(VerifierLLM):
    def __init__(self, model: str = MODEL) -> None:
        import anthropic

        self.model = model
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    def generate(self, query: str, chunks: list[str]) -> str:
        context = "\n".join(f"- {c}" for c in chunks)
        prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer using only the context."
        response = self.client.messages.create(
            model=self.model, max_tokens=200, messages=[{"role": "user", "content": prompt}]
        )
        return next(b.text for b in response.content if b.type == "text")

    def verify(self, answer: str, chunks: list[str]) -> VerificationResult:
        context = "\n".join(f"- {c}" for c in chunks)
        prompt = (
            f"Context:\n{context}\n\nProposed answer: {answer}\n\n"
            "List any claims in the proposed answer that are NOT directly supported by the "
            "context. Reply with JSON only: "
            '{"supported": true|false, "unsupported_claims": ["..."]}'
        )
        response = self.client.messages.create(
            model=self.model,
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
            output_config={
                "format": {
                    "type": "json_schema",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "supported": {"type": "boolean"},
                            "unsupported_claims": {"type": "array", "items": {"type": "string"}},
                        },
                        "required": ["supported", "unsupported_claims"],
                        "additionalProperties": False,
                    },
                }
            },
        )
        raw = next(b.text for b in response.content if b.type == "text")
        data = json.loads(raw)
        return VerificationResult(supported=data["supported"], unsupported_claims=data["unsupported_claims"])


class FakeVerifierLLM(VerifierLLM):
    # deterministic stand-in: generation stitches retrieved chunks; verification checks
    # each generated sentence has enough word overlap with some retrieved chunk
    def generate(self, query: str, chunks: list[str]) -> str:
        return " ".join(chunks) + " Also, membership costs $50 per year."  # deliberately unsupported add-on

    def verify(self, answer: str, chunks: list[str]) -> VerificationResult:
        context_words = set(" ".join(chunks).lower().split())
        sentences = [s.strip() for s in answer.split(".") if s.strip()]
        unsupported = []
        for sentence in sentences:
            words = set(sentence.lower().split())
            overlap = len(words & context_words) / max(len(words), 1)
            if overlap < 0.4:
                unsupported.append(sentence)
        return VerificationResult(supported=not unsupported, unsupported_claims=unsupported)


def self_verifying_rag(llm: VerifierLLM, query: str) -> tuple[str, VerificationResult]:
    chunks = retrieve(query)
    answer = llm.generate(query, chunks)
    verification = llm.verify(answer, chunks)
    return answer, verification


if __name__ == "__main__":
    llm: VerifierLLM = AnthropicVerifierLLM() if os.environ.get("ANTHROPIC_API_KEY") else FakeVerifierLLM()
    answer, verification = self_verifying_rag(llm, "What are the library hours and membership cost?")
    print(f"answer: {answer}")
    print(f"supported by context: {verification.supported}")
    if verification.unsupported_claims:
        print("flagged unsupported claims:")
        for claim in verification.unsupported_claims:
            print(f"  - {claim}")
