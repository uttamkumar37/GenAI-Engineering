from __future__ import annotations

import asyncio
import random
from dataclasses import dataclass


@dataclass
class LLMResponse:
    provider: str
    text: str
    latency_s: float


class MockProviderTimeoutError(Exception):
    pass


async def _call_mock_provider(provider: str, prompt: str, base_latency: float) -> LLMResponse:
    latency = base_latency + random.uniform(0, 0.3)
    await asyncio.sleep(latency)
    return LLMResponse(provider=provider, text=f"[{provider}] response to: {prompt}", latency_s=latency)


class AsyncLLMClient:
    def __init__(self, timeout_s: float = 1.0) -> None:
        self._timeout_s = timeout_s
        self._providers: dict[str, float] = {
            "claude-mock": 0.2,
            "openai-mock": 0.3,
            "gemini-mock": 0.5,
        }

    async def _call_with_timeout(self, provider: str, prompt: str) -> LLMResponse | None:
        try:
            return await asyncio.wait_for(
                _call_mock_provider(provider, prompt, self._providers[provider]),
                timeout=self._timeout_s,
            )
        except TimeoutError:
            return None

    async def call_all(self, prompt: str) -> list[LLMResponse | None]:
        tasks = [self._call_with_timeout(name, prompt) for name in self._providers]
        return await asyncio.gather(*tasks)

    async def call_fastest(self, prompt: str) -> LLMResponse:
        tasks = [
            asyncio.create_task(self._call_with_timeout(name, prompt))
            for name in self._providers
        ]
        for coro in asyncio.as_completed(tasks):
            result = await coro
            if result is not None:
                for task in tasks:
                    task.cancel()
                return result
        raise MockProviderTimeoutError("all providers timed out")


async def main() -> None:
    client = AsyncLLMClient(timeout_s=1.0)
    results = await client.call_all("What is the capital of France?")
    for result in results:
        print(result)
    fastest = await client.call_fastest("Summarize this text.")
    print("fastest:", fastest)


if __name__ == "__main__":
    asyncio.run(main())
