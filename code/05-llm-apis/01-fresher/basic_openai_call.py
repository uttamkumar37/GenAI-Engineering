# requires OPENAI_API_KEY
from __future__ import annotations

import os

from openai import OpenAI


def ask_openai(question: str, model: str = "gpt-4o-mini") -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": question}],
    )
    return response.choices[0].message.content or ""


if __name__ == "__main__":
    print(ask_openai("What is the capital of France? Answer in one sentence."))
