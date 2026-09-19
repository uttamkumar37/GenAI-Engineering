# requires ANTHROPIC_API_KEY for AnthropicLLM; FakeCitationLLM needs nothing
from __future__ import annotations

import hashlib
import os
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass

MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-opus-5")
EMBEDDING_DIM = 16


@dataclass
class Chunk:
    chunk_id: str
    text: str


CHUNKS = [
    Chunk("c1", "The Eiffel Tower was completed in 1889 for the World's Fair."),
    Chunk("c2", "It stands 330 meters tall, including antennas."),
    Chunk("c3", "The tower is located on the Champ de Mars in Paris."),
    Chunk("c4", "It was designed by engineer Gustave Eiffel's company."),
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


def retrieve(query: str, top_k: int = 3) -> list[Chunk]:
    query_vec = fake_embed(query)
    scored = [(cosine_similarity(query_vec, fake_embed(c.text)), c) for c in CHUNKS]
    scored.sort(key=lambda t: t[0], reverse=True)
    return [c for _, c in scored[:top_k]]


class CitationLLM(ABC):
    @abstractmethod
    def answer_with_citations(self, query: str, chunks: list[Chunk]) -> str: ...


class AnthropicCitationLLM(CitationLLM):
    def __init__(self, model: str = MODEL) -> None:
        import anthropic

        self.model = model
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    def answer_with_citations(self, query: str, chunks: list[Chunk]) -> str:
        context = "\n".join(f"[{c.chunk_id}] {c.text}" for c in chunks)
        prompt = (
            f"Context (each line tagged with a chunk id):\n{context}\n\nQuestion: {query}\n\n"
            "Answer using only the context. After every claim, cite the chunk id it came "
            "from in square brackets, e.g. [c1]."
        )
        response = self.client.messages.create(
            model=self.model, max_tokens=300, messages=[{"role": "user", "content": prompt}]
        )
        return next(b.text for b in response.content if b.type == "text")


class FakeCitationLLM(CitationLLM):
    # deterministic stand-in: concatenate retrieved chunks with explicit citations
    def answer_with_citations(self, query: str, chunks: list[Chunk]) -> str:
        return " ".join(f"{c.text} [{c.chunk_id}]" for c in chunks)


def extract_citations(answer: str) -> dict[str, str]:
    chunk_by_id = {c.chunk_id: c.text for c in CHUNKS}
    cited_ids = sorted(set(re.findall(r"\[(c\d+)\]", answer)))
    return {cid: chunk_by_id[cid] for cid in cited_ids if cid in chunk_by_id}


def citation_tracking_rag(llm: CitationLLM, query: str) -> tuple[str, dict[str, str]]:
    chunks = retrieve(query)
    answer = llm.answer_with_citations(query, chunks)
    return answer, extract_citations(answer)


if __name__ == "__main__":
    llm: CitationLLM = AnthropicCitationLLM() if os.environ.get("ANTHROPIC_API_KEY") else FakeCitationLLM()
    answer, citations = citation_tracking_rag(llm, "How tall is the Eiffel Tower and where is it?")
    print(f"answer: {answer}")
    print("\nsource map:")
    for chunk_id, text in citations.items():
        print(f"  {chunk_id}: {text}")
