from __future__ import annotations

import json
import time
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path

LOG_PATH = Path(__file__).with_name("llm_calls.jsonl")

# Reference per-1k-token pricing (USD) — hardcoded since there's no live billing API here.
_PRICE_PER_1K_TOKENS = {"input": 0.003, "output": 0.015}


@dataclass
class LLMCallLog:
    call_id: str
    timestamp: float
    prompt: str
    response: str
    input_tokens: int
    output_tokens: int
    latency_ms: float
    cost_usd: float


class FakeLLMClient:
    """Deterministic mock LLM client — no network calls. Stands in for a real provider SDK
    so the logging wrapper's structure (what to capture, how to compute cost) is exercised."""

    def complete(self, prompt: str) -> str:
        time.sleep(0.01)  # simulate call latency
        return f"Mock response to: {prompt[:40]}"


def _estimate_tokens(text: str) -> int:
    return max(1, len(text.split()))  # crude word-count proxy for a real tokenizer


def _estimate_cost(input_tokens: int, output_tokens: int) -> float:
    return (input_tokens / 1000) * _PRICE_PER_1K_TOKENS["input"] + (
        output_tokens / 1000
    ) * _PRICE_PER_1K_TOKENS["output"]


def logged_complete(client: FakeLLMClient, prompt: str, log_path: Path = LOG_PATH) -> str:
    start = time.perf_counter()
    response = client.complete(prompt)
    latency_ms = (time.perf_counter() - start) * 1000

    input_tokens = _estimate_tokens(prompt)
    output_tokens = _estimate_tokens(response)

    log_entry = LLMCallLog(
        call_id=str(uuid.uuid4()),
        timestamp=time.time(),
        prompt=prompt,
        response=response,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        latency_ms=round(latency_ms, 2),
        cost_usd=round(_estimate_cost(input_tokens, output_tokens), 6),
    )

    with log_path.open("a") as f:
        f.write(json.dumps(asdict(log_entry)) + "\n")

    return response


if __name__ == "__main__":
    client = FakeLLMClient()
    prompts = [
        "Summarize the benefits of structured LLM call logging.",
        "What fields matter most for LLM observability?",
    ]

    for prompt in prompts:
        response = logged_complete(client, prompt)
        print(f"PROMPT: {prompt}\nRESPONSE: {response}\n")

    print(f"Structured logs written to: {LOG_PATH}")
    print("\nLast entries:")
    with LOG_PATH.open() as f:
        for line in f.readlines()[-2:]:
            print(" ", line.strip())
