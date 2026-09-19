# requires ANTHROPIC_API_KEY
from __future__ import annotations

import os

import anthropic


def ask_claude(question: str, model: str = "claude-opus-5") -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    response = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[{"role": "user", "content": question}],
    )
    return next(block.text for block in response.content if block.type == "text")


if __name__ == "__main__":
    print(ask_claude("What is the capital of France? Answer in one sentence."))
