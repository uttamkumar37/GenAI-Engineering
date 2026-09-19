from __future__ import annotations

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LLMResponse:
    text: str
    input_tokens: int
    output_tokens: int
    model: str
    provider: str
    cache_read_tokens: int = 0


class ProviderError(Exception):
    pass


class LLMProvider(ABC):
    name: str

    @abstractmethod
    def generate(
        self,
        messages: list[dict],
        system: str | None = None,
        cacheable_system: bool = False,
        max_tokens: int = 1024,
    ) -> LLMResponse: ...


class ClaudeProvider(LLMProvider):
    # requires ANTHROPIC_API_KEY
    name = "anthropic"

    def __init__(self, model: str = "claude-opus-5") -> None:
        import anthropic

        self.model = model
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        self._anthropic = anthropic

    def generate(
        self,
        messages: list[dict],
        system: str | None = None,
        cacheable_system: bool = False,
        max_tokens: int = 1024,
    ) -> LLMResponse:
        try:
            system_param: str | list[dict] | None = system
            if system and cacheable_system:
                system_param = [
                    {"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}
                ]
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system_param,
                messages=messages,
            )
            text = next((b.text for b in response.content if b.type == "text"), "")
            return LLMResponse(
                text=text,
                input_tokens=response.usage.input_tokens,
                output_tokens=response.usage.output_tokens,
                cache_read_tokens=getattr(response.usage, "cache_read_input_tokens", 0) or 0,
                model=self.model,
                provider=self.name,
            )
        except self._anthropic.APIError as exc:
            raise ProviderError(str(exc)) from exc


class OpenAIProvider(LLMProvider):
    # requires OPENAI_API_KEY
    name = "openai"

    def __init__(self, model: str = "gpt-4o-mini") -> None:
        import openai

        self.model = model
        self.client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self._openai = openai

    def generate(
        self,
        messages: list[dict],
        system: str | None = None,
        cacheable_system: bool = False,
        max_tokens: int = 1024,
    ) -> LLMResponse:
        try:
            chat_messages = ([{"role": "system", "content": system}] if system else []) + messages
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=chat_messages,
            )
            usage = response.usage
            return LLMResponse(
                text=response.choices[0].message.content or "",
                input_tokens=usage.prompt_tokens if usage else 0,
                output_tokens=usage.completion_tokens if usage else 0,
                model=self.model,
                provider=self.name,
            )
        except self._openai.APIError as exc:
            raise ProviderError(str(exc)) from exc


class FakeProvider(LLMProvider):
    # deterministic offline stand-in for testing the gateway without credentials
    def __init__(self, name: str = "fake", model: str = "fake-model", fail: bool = False) -> None:
        self.name = name
        self.model = model
        self.fail = fail

    def generate(
        self,
        messages: list[dict],
        system: str | None = None,
        cacheable_system: bool = False,
        max_tokens: int = 1024,
    ) -> LLMResponse:
        if self.fail:
            raise ProviderError(f"{self.name} is simulating an outage")
        last_user = next(
            (m["content"] for m in reversed(messages) if m["role"] == "user"), ""
        )
        text = f"[{self.name}] fake reply to: {last_user[:60]}"
        return LLMResponse(
            text=text,
            input_tokens=max(len(str(messages)) // 4, 1),
            output_tokens=max(len(text) // 4, 1),
            model=self.model,
            provider=self.name,
        )


class OllamaProvider(LLMProvider):
    # requires a local Ollama server; no API key needed
    name = "ollama"

    def __init__(self, model: str = "llama3.2", host: str = "http://localhost:11434") -> None:
        import ollama

        self.model = model
        self.client = ollama.Client(host=host)
        self._ollama = ollama

    def generate(
        self,
        messages: list[dict],
        system: str | None = None,
        cacheable_system: bool = False,
        max_tokens: int = 1024,
    ) -> LLMResponse:
        try:
            chat_messages = ([{"role": "system", "content": system}] if system else []) + messages
            response = self.client.chat(
                model=self.model,
                messages=chat_messages,
                options={"num_predict": max_tokens},
            )
            return LLMResponse(
                text=response["message"]["content"],
                input_tokens=response.get("prompt_eval_count", 0),
                output_tokens=response.get("eval_count", 0),
                model=self.model,
                provider=self.name,
            )
        except self._ollama.ResponseError as exc:
            raise ProviderError(str(exc)) from exc
