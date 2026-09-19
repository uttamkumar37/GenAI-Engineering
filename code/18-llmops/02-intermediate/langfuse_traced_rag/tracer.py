from __future__ import annotations

import json
import os
import time
import uuid
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from typing import Iterator


@dataclass
class Span:
    span_id: str
    name: str
    start_time: float
    end_time: float | None = None
    metadata: dict = field(default_factory=dict)
    children: list["Span"] = field(default_factory=list)

    @property
    def duration_ms(self) -> float | None:
        if self.end_time is None:
            return None
        return round((self.end_time - self.start_time) * 1000, 2)


class FallbackTracer:
    """Minimal in-process tracer used when Langfuse isn't configured (no LANGFUSE_* env vars,
    or the `langfuse` package isn't installed). Logs structured, nested spans to stdout/JSON
    so the tracing demo runs standalone without any external service."""

    def __init__(self) -> None:
        self.root_spans: list[Span] = []
        self._stack: list[Span] = []

    @contextmanager
    def span(self, name: str, **metadata) -> Iterator[Span]:
        s = Span(span_id=str(uuid.uuid4())[:8], name=name, start_time=time.perf_counter(), metadata=metadata)
        if self._stack:
            self._stack[-1].children.append(s)
        else:
            self.root_spans.append(s)
        self._stack.append(s)
        try:
            yield s
        finally:
            s.end_time = time.perf_counter()
            self._stack.pop()

    def as_dict(self) -> list[dict]:
        def to_dict(span: Span) -> dict:
            d = asdict(span)
            d["duration_ms"] = span.duration_ms
            d["children"] = [to_dict(c) for c in span.children]
            return d

        return [to_dict(s) for s in self.root_spans]

    def print_tree(self) -> None:
        def _print(span: Span, depth: int) -> None:
            print(f"{'  ' * depth}- {span.name} ({span.duration_ms}ms) {span.metadata}")
            for child in span.children:
                _print(child, depth + 1)

        for root in self.root_spans:
            _print(root, 0)


class LangfuseTracer:
    """Thin wrapper around the real `langfuse` SDK client (requires LANGFUSE_PUBLIC_KEY /
    LANGFUSE_SECRET_KEY env vars + `pip install langfuse`). Written against the langfuse
    `Langfuse().trace()` / `.span()` client API as of langfuse-python 2.x — verify against
    your installed version, since the SDK has moved toward `@observe`-decorator patterns too."""

    def __init__(self) -> None:
        from langfuse import Langfuse  # type: ignore

        self._client = Langfuse()
        self._trace = None
        self._stack: list = []

    @contextmanager
    def span(self, name: str, **metadata) -> Iterator[object]:
        if self._trace is None:
            self._trace = self._client.trace(name="rag_pipeline")
            parent = self._trace
        else:
            parent = self._stack[-1] if self._stack else self._trace

        span_obj = parent.span(name=name, metadata=metadata)
        self._stack.append(span_obj)
        try:
            yield span_obj
        finally:
            span_obj.end()
            self._stack.pop()


def get_tracer():
    has_langfuse_config = bool(os.environ.get("LANGFUSE_PUBLIC_KEY") and os.environ.get("LANGFUSE_SECRET_KEY"))
    if has_langfuse_config:
        try:
            return LangfuseTracer()
        except ImportError:
            pass
    return FallbackTracer()


if __name__ == "__main__":
    tracer = get_tracer()
    print(f"Using tracer: {type(tracer).__name__}")

    with tracer.span("rag_request", question="What is PagedAttention?"):
        with tracer.span("retrieval", k=3):
            time.sleep(0.01)
        with tracer.span("generation", model="mock-llm"):
            time.sleep(0.02)

    if isinstance(tracer, FallbackTracer):
        tracer.print_tree()
        print("\nJSON export:")
        print(json.dumps(tracer.as_dict(), indent=2))
