from __future__ import annotations

import sys
import time
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "02-intermediate"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "02-intermediate" / "langfuse_traced_rag"))

from semantic_cache import FakeEmbedder, FakeLLM, SemanticCache  # noqa: E402
from tracer import get_tracer  # noqa: E402


@dataclass
class RequestOutcome:
    prompt: str
    response: str
    cache_hit: bool
    latency_ms: float
    cost_usd: float
    quality_score: float


class FallbackChain:
    """Ordered list of LLM clients; falls through to the next on failure (built in Topic 05,
    now wired into full observability so every attempt — success or failure — is traced)."""

    def __init__(self, clients: list) -> None:
        self._clients = clients

    def complete(self, prompt: str, tracer) -> tuple[str, str]:
        last_error: Exception | None = None
        for client in self._clients:
            name = type(client).__name__
            with tracer.span("fallback_attempt", provider=name):
                try:
                    return client.complete(prompt), name
                except Exception as exc:  # noqa: BLE001
                    last_error = exc
                    continue
        raise RuntimeError(f"All providers failed: {last_error}")


class FlakyLLM:
    def __init__(self, fail_on_word: str) -> None:
        self._fail_on_word = fail_on_word

    def complete(self, prompt: str) -> str:
        if self._fail_on_word in prompt.lower():
            raise RuntimeError("simulated provider outage")
        return f"PrimaryProvider answer: {prompt}"


class BackupLLM:
    def complete(self, prompt: str) -> str:
        return f"BackupProvider answer: {prompt}"


def _mock_quality_score(response: str) -> float:
    return round(min(1.0, len(response.split()) / 20), 2)


_PRICE_PER_1K_TOKENS = 0.006


class LLMOpsService:
    """Ties together tracing, semantic caching, a fallback chain, and cost/quality metrics
    into one wrapper — the pieces a production LLM service needs before real user traffic."""

    def __init__(self) -> None:
        self._tracer = get_tracer()
        self._cache = SemanticCache(FakeEmbedder(), similarity_threshold=0.75)
        self._fallback = FallbackChain([FlakyLLM(fail_on_word="outage"), BackupLLM()])
        self.request_log: list[RequestOutcome] = []

    def handle_request(self, prompt: str) -> RequestOutcome:
        start = time.perf_counter()
        with self._tracer.span("request", prompt=prompt):
            cached_response, score = self._cache.get(prompt)
            cache_hit = cached_response is not None

            with self._tracer.span("generation", cache_hit=cache_hit, similarity=round(score, 2)):
                if cache_hit:
                    response = cached_response
                else:
                    response, provider = self._fallback.complete(prompt, self._tracer)
                    self._cache.set(prompt, response)

        latency_ms = round((time.perf_counter() - start) * 1000, 2)
        tokens = len(prompt.split()) + len(response.split())
        cost_usd = 0.0 if cache_hit else round((tokens / 1000) * _PRICE_PER_1K_TOKENS, 6)
        quality_score = _mock_quality_score(response)

        outcome = RequestOutcome(prompt, response, cache_hit, latency_ms, cost_usd, quality_score)
        self.request_log.append(outcome)
        return outcome

    def dashboard_summary(self) -> dict:
        if not self.request_log:
            return {}
        total_cost = sum(r.cost_usd for r in self.request_log)
        avg_latency = sum(r.latency_ms for r in self.request_log) / len(self.request_log)
        avg_quality = sum(r.quality_score for r in self.request_log) / len(self.request_log)
        cache_hit_rate = sum(r.cache_hit for r in self.request_log) / len(self.request_log)
        return {
            "num_requests": len(self.request_log),
            "total_cost_usd": round(total_cost, 6),
            "avg_latency_ms": round(avg_latency, 2),
            "avg_quality_score": round(avg_quality, 3),
            "cache_hit_rate": round(cache_hit_rate, 2),
        }


if __name__ == "__main__":
    service = LLMOpsService()

    requests = [
        "What is the refund policy?",
        "What is the refund policy?",  # exact repeat -> cache hit
        "There is an outage affecting checkout",  # triggers primary failure -> fallback
        "What's your refund policy?",  # near-duplicate -> cache hit
    ]

    for prompt in requests:
        outcome = service.handle_request(prompt)
        print(
            f"cache_hit={outcome.cache_hit!s:5s} latency={outcome.latency_ms:6.2f}ms "
            f"cost=${outcome.cost_usd:.6f} quality={outcome.quality_score} "
            f"prompt={prompt!r}"
        )

    print("\nDashboard summary:")
    for key, value in service.dashboard_summary().items():
        print(f"  {key}: {value}")
