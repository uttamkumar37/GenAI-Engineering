from __future__ import annotations

import os

from .gateway import UnifiedLLMGateway
from .providers import ClaudeProvider, FakeProvider, OllamaProvider, OpenAIProvider


def build_real_chain() -> list:
    # Claude -> OpenAI -> local Ollama, in preference order
    chain = []
    if os.environ.get("ANTHROPIC_API_KEY"):
        chain.append(ClaudeProvider())
    if os.environ.get("OPENAI_API_KEY"):
        chain.append(OpenAIProvider())
    chain.append(OllamaProvider())
    return chain


def demo_offline_fallback() -> None:
    # first provider "fails", gateway falls back to the second automatically
    chain = [FakeProvider("primary-down", fail=True), FakeProvider("secondary-ok")]
    gateway = UnifiedLLMGateway(fallback_chain=chain)
    result = gateway.complete(
        messages=[{"role": "user", "content": "Summarize the plot of Hamlet."}],
        system="You are a terse literary assistant.",
        cacheable_system=True,
    )
    print(f"provider used: {result.provider_used}")
    print(f"attempts: {result.attempts}")
    print(f"estimated cost: ${result.estimated_cost_usd}")
    print(f"reply: {result.response.text}")


if __name__ == "__main__":
    demo_offline_fallback()
