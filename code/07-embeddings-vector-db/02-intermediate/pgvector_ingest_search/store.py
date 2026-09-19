# PgVectorStore requires PGVECTOR_DSN (Postgres with the pgvector extension) + psycopg[binary] + pgvector
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class SearchResult:
    doc_id: str
    text: str
    metadata: dict[str, Any]
    score: float


class VectorStore(ABC):
    @abstractmethod
    def upsert(
        self, ids: list[str], vectors: list[list[float]], texts: list[str], metadatas: list[dict[str, Any]]
    ) -> None: ...

    @abstractmethod
    def search(
        self, query_vector: list[float], top_k: int = 5, metadata_filter: dict[str, Any] | None = None
    ) -> list[SearchResult]: ...


class InMemoryVectorStore(VectorStore):
    def __init__(self) -> None:
        self._rows: dict[str, tuple[list[float], str, dict[str, Any]]] = {}

    def upsert(
        self, ids: list[str], vectors: list[list[float]], texts: list[str], metadatas: list[dict[str, Any]]
    ) -> None:
        for doc_id, vector, text, metadata in zip(ids, vectors, texts, metadatas):
            self._rows[doc_id] = (vector, text, metadata)

    @staticmethod
    def _cosine(a: list[float], b: list[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(y * y for y in b) ** 0.5
        return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0

    def search(
        self, query_vector: list[float], top_k: int = 5, metadata_filter: dict[str, Any] | None = None
    ) -> list[SearchResult]:
        results = []
        for doc_id, (vector, text, metadata) in self._rows.items():
            if metadata_filter and not all(metadata.get(k) == v for k, v in metadata_filter.items()):
                continue
            score = self._cosine(query_vector, vector)
            results.append(SearchResult(doc_id=doc_id, text=text, metadata=metadata, score=score))
        results.sort(key=lambda r: r.score, reverse=True)
        return results[:top_k]


@dataclass
class PgVectorStore(VectorStore):
    dsn: str
    table: str = "document_chunks"
    dim: int = 32
    _conn: Any = field(default=None, init=False, repr=False)

    def _connect(self):
        import psycopg
        from pgvector.psycopg import register_vector

        if self._conn is None:
            self._conn = psycopg.connect(self.dsn, autocommit=True)
            self._conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
            register_vector(self._conn)
            self._conn.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.table} (
                    id TEXT PRIMARY KEY,
                    text TEXT NOT NULL,
                    metadata JSONB NOT NULL DEFAULT '{{}}',
                    embedding VECTOR({self.dim})
                )
                """
            )
        return self._conn

    def upsert(
        self, ids: list[str], vectors: list[list[float]], texts: list[str], metadatas: list[dict[str, Any]]
    ) -> None:
        import json

        conn = self._connect()
        with conn.cursor() as cur:
            for doc_id, vector, text, metadata in zip(ids, vectors, texts, metadatas):
                cur.execute(
                    f"""
                    INSERT INTO {self.table} (id, text, metadata, embedding)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET text = EXCLUDED.text,
                        metadata = EXCLUDED.metadata, embedding = EXCLUDED.embedding
                    """,
                    (doc_id, text, json.dumps(metadata), vector),
                )

    def search(
        self, query_vector: list[float], top_k: int = 5, metadata_filter: dict[str, Any] | None = None
    ) -> list[SearchResult]:
        import json

        conn = self._connect()
        where_clause = "WHERE metadata @> %s" if metadata_filter else ""
        params: list[Any] = [query_vector]
        if metadata_filter:
            params.append(json.dumps(metadata_filter))
        params.extend([query_vector, top_k])
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT id, text, metadata, 1 - (embedding <=> %s) AS score
                FROM {self.table}
                {where_clause}
                ORDER BY embedding <=> %s
                LIMIT %s
                """,
                params,
            )
            rows = cur.fetchall()
        return [
            SearchResult(doc_id=row[0], text=row[1], metadata=row[2], score=float(row[3]))
            for row in rows
        ]
