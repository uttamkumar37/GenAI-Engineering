from __future__ import annotations

import asyncio

from .circuit_breaker import CircuitBreaker, CircuitOpenError
from .provider import CompletionResult, LLMProvider, ProviderError


class ResilientLLMClient:
    def __init__(
        self,
        providers: list[LLMProvider],
        max_concurrent_calls: int = 5,
        failure_threshold: int = 3,
        reset_timeout_s: float = 5.0,
    ) -> None:
        self._providers = providers
        self._semaphore = asyncio.Semaphore(max_concurrent_calls)
        self._breakers = {
            provider.name: CircuitBreaker(failure_threshold, reset_timeout_s) for provider in providers
        }

    async def _call_provider(self, provider: LLMProvider, prompt: str) -> CompletionResult:
        breaker = self._breakers[provider.name]
        breaker.before_call()
        async with self._semaphore:
            try:
                result = await provider.complete(prompt)
            except ProviderError:
                breaker.record_failure()
                raise
            else:
                breaker.record_success()
                return result

    async def complete_with_fallback(self, prompt: str) -> CompletionResult:
        last_error: Exception | None = None
        for provider in self._providers:
            try:
                return await self._call_provider(provider, prompt)
            except (ProviderError, CircuitOpenError) as error:
                last_error = error
                continue
        raise ProviderError(f"all providers failed: {last_error}")

    async def complete_many(self, prompts: list[str]) -> list[CompletionResult | BaseException]:
        tasks = [self.complete_with_fallback(prompt) for prompt in prompts]
        return await asyncio.gather(*tasks, return_exceptions=True)
