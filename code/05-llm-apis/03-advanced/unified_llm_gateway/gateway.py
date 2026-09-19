from __future__ import annotations

import random
import time
from dataclasses import dataclass, field

from .cost import estimate_cost
from .providers import LLMProvider, LLMResponse, ProviderError


@dataclass
class GatewayResult:
    response: LLMResponse
    estimated_cost_usd: float
    attempts: int
    provider_used: str


@dataclass
class UnifiedLLMGateway:
    fallback_chain: list[LLMProvider]
    max_retries_per_provider: int = 3
    base_delay: float = 0.5
    max_delay: float = 8.0

    _last_errors: list[str] = field(default_factory=list, init=False)

    def _call_with_backoff(
        self, provider: LLMProvider, **kwargs
    ) -> LLMResponse:
        last_exc: Exception | None = None
        for attempt in range(self.max_retries_per_provider):
            try:
                return provider.generate(**kwargs)
            except ProviderError as exc:
                last_exc = exc
                delay = min(self.base_delay * (2**attempt) + random.uniform(0, 0.25), self.max_delay)
                self._last_errors.append(f"{provider.name} attempt {attempt + 1}: {exc}")
                time.sleep(delay)
        assert last_exc is not None
        raise last_exc

    def complete(
        self,
        messages: list[dict],
        system: str | None = None,
        cacheable_system: bool = False,
        max_tokens: int = 1024,
    ) -> GatewayResult:
        self._last_errors = []
        total_attempts = 0
        for provider in self.fallback_chain:
            try:
                response = self._call_with_backoff(
                    provider,
                    messages=messages,
                    system=system,
                    cacheable_system=cacheable_system,
                    max_tokens=max_tokens,
                )
                total_attempts += 1
                cost = estimate_cost(
                    response.model,
                    response.input_tokens,
                    response.output_tokens,
                    response.cache_read_tokens,
                )
                return GatewayResult(
                    response=response,
                    estimated_cost_usd=cost,
                    attempts=total_attempts,
                    provider_used=provider.name,
                )
            except ProviderError:
                total_attempts += self.max_retries_per_provider
                continue
        raise RuntimeError(
            f"All providers in fallback chain failed. Errors: {self._last_errors}"
        )
