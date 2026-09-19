from __future__ import annotations

import time
from dataclasses import dataclass


@dataclass
class LatencyResult:
    prompt: str
    num_tokens: int
    total_seconds: float

    @property
    def seconds_per_token(self) -> float:
        return self.total_seconds / max(self.num_tokens, 1)

    @property
    def tokens_per_second(self) -> float:
        return self.num_tokens / max(self.total_seconds, 1e-9)


class LocalHFModel:
    """Wraps transformers `generate()`; falls back to a fake tokenizer/model if
    `transformers`/torch/weights aren't available in this sandbox (no GPU/network here)."""

    def __init__(self, model_name: str = "sshleifer/tiny-gpt2") -> None:
        self.model_name = model_name
        self._backend = None
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer  # type: ignore

            self._tokenizer = AutoTokenizer.from_pretrained(model_name)
            self._model = AutoModelForCausalLM.from_pretrained(model_name)
            self._backend = "transformers"
        except Exception:
            self._backend = "fake"

    def generate(self, prompt: str, max_new_tokens: int = 32) -> tuple[str, int]:
        if self._backend == "transformers":
            inputs = self._tokenizer(prompt, return_tensors="pt")
            output_ids = self._model.generate(
                **inputs, max_new_tokens=max_new_tokens, do_sample=False
            )
            generated = output_ids[0][inputs["input_ids"].shape[-1] :]
            text = self._tokenizer.decode(generated, skip_special_tokens=True)
            return text, len(generated)
        # fake backend: deterministic word-repeat generator, same token accounting shape
        words = (prompt.split() or ["lorem"])
        generated_words = [words[i % len(words)] for i in range(max_new_tokens)]
        time.sleep(0.001 * max_new_tokens)  # simulate per-token compute cost
        return " ".join(generated_words), max_new_tokens


def measure_latency(model: LocalHFModel, prompt: str, max_new_tokens: int = 32) -> LatencyResult:
    start = time.perf_counter()
    _, num_tokens = model.generate(prompt, max_new_tokens=max_new_tokens)
    elapsed = time.perf_counter() - start
    return LatencyResult(prompt=prompt, num_tokens=num_tokens, total_seconds=elapsed)


if __name__ == "__main__":
    model = LocalHFModel()
    print(f"backend: {model._backend}, model: {model.model_name}")

    prompts = [
        "Explain what a KV cache is in one sentence.",
        "Summarize the benefits of continuous batching.",
        "List three reasons LLM serving differs from REST APIs.",
    ]

    for prompt in prompts:
        result = measure_latency(model, prompt, max_new_tokens=24)
        print(
            f"tokens={result.num_tokens:3d}  "
            f"total={result.total_seconds * 1000:7.2f}ms  "
            f"per_token={result.seconds_per_token * 1000:6.3f}ms  "
            f"tok/s={result.tokens_per_second:7.2f}  "
            f"prompt={prompt[:40]!r}"
        )
