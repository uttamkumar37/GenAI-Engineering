from __future__ import annotations

from dataclasses import dataclass

# self-contained stand-in for the (not-yet-implemented) Topic 07/08 embeddings+RAG pipeline —
# uses keyword-overlap "retrieval" instead of real embeddings so this module has zero
# external dependencies


@dataclass(frozen=True)
class Chunk:
    doc_id: str
    text: str
    source: str


CORPUS = [
    Chunk("kb-001", "MCP servers expose tools, resources, and prompts to any compatible client.", "mcp-spec.md"),
    Chunk("kb-002", "Rate limiting and input validation are essential when exposing internal data via MCP.", "security-notes.md"),
    Chunk("kb-003", "RAG pipelines retrieve relevant chunks then feed them into the model's context window.", "rag-overview.md"),
    Chunk("kb-004", "Citations should reference the original source document, not just the retrieved chunk.", "rag-overview.md"),
]


def retrieve(query: str, top_k: int = 2) -> list[Chunk]:
    query_words = set(query.lower().split())
    scored = [(len(query_words & set(c.text.lower().split())), c) for c in CORPUS]
    scored = [pair for pair in scored if pair[0] > 0]
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [chunk for _, chunk in scored[:top_k]]
