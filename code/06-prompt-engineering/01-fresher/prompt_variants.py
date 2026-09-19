# requires ANTHROPIC_API_KEY
from __future__ import annotations

import os

import anthropic

MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-opus-5")
TASK = "Classify the sentiment of this review as positive, negative, or neutral: 'The battery life is decent but the screen is disappointing.'"

FEW_SHOT_EXAMPLES = """Review: "Absolutely love this product, works perfectly!"
Sentiment: positive

Review: "Broke after two days, total waste of money."
Sentiment: negative

Review: "It's fine, does what it says, nothing special."
Sentiment: neutral"""


def zero_shot(client: anthropic.Anthropic) -> str:
    response = client.messages.create(
        model=MODEL, max_tokens=50, messages=[{"role": "user", "content": TASK}]
    )
    return next(b.text for b in response.content if b.type == "text")


def few_shot(client: anthropic.Anthropic) -> str:
    prompt = f"{FEW_SHOT_EXAMPLES}\n\n{TASK}"
    response = client.messages.create(
        model=MODEL, max_tokens=50, messages=[{"role": "user", "content": prompt}]
    )
    return next(b.text for b in response.content if b.type == "text")


def with_system_prompt(client: anthropic.Anthropic) -> str:
    response = client.messages.create(
        model=MODEL,
        max_tokens=50,
        system="You are a sentiment classifier. Respond with exactly one word: positive, negative, or neutral.",
        messages=[{"role": "user", "content": TASK}],
    )
    return next(b.text for b in response.content if b.type == "text")


if __name__ == "__main__":
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    print("zero-shot:      ", zero_shot(client))
    print("few-shot:       ", few_shot(client))
    print("with system:    ", with_system_prompt(client))
