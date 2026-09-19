# requires ANTHROPIC_API_KEY for the real client; FakeLLMClient needs nothing
from __future__ import annotations

import os
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass

MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-opus-5")


@dataclass
class EvalCase:
    input_text: str
    expected_keyword: str


EVAL_SET = [
    EvalCase("The package arrived broken and support never replied.", "negative"),
    EvalCase("Fast shipping and the product works exactly as advertised.", "positive"),
    EvalCase("It's an average blender, nothing more nothing less.", "neutral"),
]

PROMPT_VARIANTS = {
    "plain": "Classify the sentiment (positive/negative/neutral) of: {text}",
    "role_primed": (
        "You are an expert sentiment analyst. Classify the sentiment "
        "(respond with exactly one word: positive, negative, or neutral) of: {text}"
    ),
    "few_shot": (
        'Review: "Terrible, broke in a day." -> negative\n'
        'Review: "Great value for money!" -> positive\n'
        'Review: "{text}" ->'
    ),
}


class LLMClient(ABC):
    @abstractmethod
    def complete(self, prompt: str) -> str: ...


class AnthropicLLMClient(LLMClient):
    def __init__(self, model: str = MODEL) -> None:
        import anthropic

        self.model = model
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    def complete(self, prompt: str) -> str:
        response = self.client.messages.create(
            model=self.model, max_tokens=20, messages=[{"role": "user", "content": prompt}]
        )
        return next(b.text for b in response.content if b.type == "text")


class FakeLLMClient(LLMClient):
    # deterministic lexicon-based sentiment classifier, no network required
    _POSITIVE = {"great", "fast", "love", "excellent", "works"}
    _NEGATIVE = {"broken", "terrible", "never", "bad", "worst"}

    def complete(self, prompt: str) -> str:
        text = prompt.lower()
        pos = sum(word in text for word in self._POSITIVE)
        neg = sum(word in text for word in self._NEGATIVE)
        if pos > neg:
            return "positive"
        if neg > pos:
            return "negative"
        return "neutral"


def score_variant(client: LLMClient, template: str, cases: list[EvalCase]) -> float:
    correct = 0
    for case in cases:
        prompt = template.format(text=case.input_text)
        output = client.complete(prompt).strip().lower()
        if re.search(rf"\b{case.expected_keyword}\b", output):
            correct += 1
    return correct / len(cases)


def run_ab_test(client: LLMClient) -> dict[str, float]:
    return {name: score_variant(client, template, EVAL_SET) for name, template in PROMPT_VARIANTS.items()}


if __name__ == "__main__":
    client: LLMClient = AnthropicLLMClient() if os.environ.get("ANTHROPIC_API_KEY") else FakeLLMClient()
    scores = run_ab_test(client)
    for name, score in sorted(scores.items(), key=lambda kv: -kv[1]):
        print(f"{name:12s} accuracy={score:.2f}")
    winner = max(scores, key=scores.get)
    print(f"\nwinner: {winner}")
