from __future__ import annotations

import re

DOCUMENT = """
Retrieval-Augmented Generation (RAG) combines a retriever with a generator.
The retriever finds relevant chunks of text from a knowledge base. The generator
then uses those chunks as context to produce a grounded answer.

Chunking strategy matters a lot. Fixed-size chunking splits text every N
characters regardless of structure, which is simple but can cut sentences in
half. Recursive chunking tries larger separators first (paragraphs, then
sentences, then words) before falling back to a hard split, preserving more
natural boundaries.

Semantic chunking goes further: it embeds individual sentences and groups
consecutive sentences together only while they stay topically similar,
starting a new chunk when the topic shifts. This tends to produce more
coherent chunks at the cost of extra embedding calls.
"""


def fixed_size_chunks(text: str, size: int = 200, overlap: int = 20) -> list[str]:
    text = text.strip()
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start += size - overlap
    return chunks


def recursive_chunks(text: str, max_size: int = 200) -> list[str]:
    separators = ["\n\n", "\n", ". ", " "]

    def split(chunk: str, seps: list[str]) -> list[str]:
        if len(chunk) <= max_size or not seps:
            return [chunk]
        sep, rest = seps[0], seps[1:]
        parts = [p for p in chunk.split(sep) if p]
        result: list[str] = []
        buffer = ""
        for part in parts:
            candidate = (buffer + sep + part) if buffer else part
            if len(candidate) <= max_size:
                buffer = candidate
            else:
                if buffer:
                    result.append(buffer)
                buffer = part
        if buffer:
            result.append(buffer)
        final: list[str] = []
        for piece in result:
            if len(piece) > max_size:
                final.extend(split(piece, rest))
            else:
                final.append(piece)
        return final

    return [c.strip() for c in split(text.strip(), separators) if c.strip()]


def _fake_sentence_embedding(sentence: str) -> set[str]:
    # deterministic bag-of-words stand-in for a real sentence embedding
    return {w.lower().strip(".,") for w in sentence.split() if len(w) > 3}


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def semantic_chunks(text: str, similarity_threshold: float = 0.12) -> list[str]:
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]
    if not sentences:
        return []
    chunks: list[list[str]] = [[sentences[0]]]
    prev_embedding = _fake_sentence_embedding(sentences[0])
    for sentence in sentences[1:]:
        embedding = _fake_sentence_embedding(sentence)
        if _jaccard(prev_embedding, embedding) >= similarity_threshold:
            chunks[-1].append(sentence)
        else:
            chunks.append([sentence])
        prev_embedding = embedding
    return [" ".join(c) for c in chunks]


if __name__ == "__main__":
    for name, chunks in [
        ("fixed-size", fixed_size_chunks(DOCUMENT)),
        ("recursive", recursive_chunks(DOCUMENT)),
        ("semantic", semantic_chunks(DOCUMENT)),
    ]:
        print(f"\n=== {name}: {len(chunks)} chunks ===")
        for i, chunk in enumerate(chunks):
            print(f"[{i}] ({len(chunk)} chars) {chunk[:80]!r}")
