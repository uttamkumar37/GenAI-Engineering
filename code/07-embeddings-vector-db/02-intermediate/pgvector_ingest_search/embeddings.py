# requires OPENAI_API_KEY for OpenAIEmbeddingClient; FakeEmbeddingClient needs nothing
from __future__ import annotations

import hashlib
import os
from abc import ABC, abstractmethod

EMBEDDING_DIM = 32


class EmbeddingClient(ABC):
    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]: ...


class OpenAIEmbeddingClient(EmbeddingClient):
    def __init__(self, model: str = "text-embedding-3-small") -> None:
        from openai import OpenAI

        self.model = model
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def embed(self, texts: list[str]) -> list[list[float]]:
        response = self.client.embeddings.create(model=self.model, input=texts)
        return [item.embedding for item in response.data]


class FakeEmbeddingClient(EmbeddingClient):
    # deterministic hash-based pseudo-embedding: same text always maps to the same vector
    def embed(self, texts: list[str]) -> list[list[float]]:
        return [self._embed_one(text) for text in texts]

    def _embed_one(self, text: str) -> list[float]:
        vector = []
        for i in range(EMBEDDING_DIM):
            digest = hashlib.sha256(f"{text}:{i}".encode()).digest()
            vector.append((digest[0] / 255.0) * 2 - 1)
        return vector
