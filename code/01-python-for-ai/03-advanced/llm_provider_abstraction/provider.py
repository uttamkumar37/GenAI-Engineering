from __future__ import annotations

import abc
import asyncio
import random
from dataclasses import dataclass


@dataclass
class CompletionResult:
    provider: str
    text: str


class ProviderError(Exception):
    pass


class LLMProvider(abc.ABC):
    name: str

    @abc.abstractmethod
    async def complete(self, prompt: str) -> CompletionResult: ...


class MockClaudeProvider(LLMProvider):
    name = "claude-mock"

    def __init__(self, failure_rate: float = 0.0) -> None:
        self._failure_rate = failure_rate

    async def complete(self, prompt: str) -> CompletionResult:
        await asyncio.sleep(0.05)
        if random.random() < self._failure_rate:
            raise ProviderError(f"{self.name} failed")
        return CompletionResult(provider=self.name, text=f"[{self.name}] {prompt}")


class MockOpenAIProvider(LLMProvider):
    name = "openai-mock"

    def __init__(self, failure_rate: float = 0.0) -> None:
        self._failure_rate = failure_rate

    async def complete(self, prompt: str) -> CompletionResult:
        await asyncio.sleep(0.05)
        if random.random() < self._failure_rate:
            raise ProviderError(f"{self.name} failed")
        return CompletionResult(provider=self.name, text=f"[{self.name}] {prompt}")


class MockGeminiProvider(LLMProvider):
    name = "gemini-mock"

    def __init__(self, failure_rate: float = 0.0) -> None:
        self._failure_rate = failure_rate

    async def complete(self, prompt: str) -> CompletionResult:
        await asyncio.sleep(0.05)
        if random.random() < self._failure_rate:
            raise ProviderError(f"{self.name} failed")
        return CompletionResult(provider=self.name, text=f"[{self.name}] {prompt}")
