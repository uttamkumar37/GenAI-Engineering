# requires ANTHROPIC_API_KEY
from __future__ import annotations

import os

import anthropic

MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-opus-5")


class ChatSession:
    def __init__(self, client: anthropic.Anthropic, system: str | None = None) -> None:
        self.client = client
        self.system = system
        self.history: list[dict] = []

    def send(self, user_message: str) -> str:
        self.history.append({"role": "user", "content": user_message})
        chunks: list[str] = []
        with self.client.messages.stream(
            model=MODEL,
            max_tokens=2048,
            system=self.system,
            messages=self.history,
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
                chunks.append(text)
            final = stream.get_final_message()
        print()
        reply = "".join(chunks) or next(
            (b.text for b in final.content if b.type == "text"), ""
        )
        self.history.append({"role": "assistant", "content": reply})
        return reply


def run_cli() -> None:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    session = ChatSession(client, system="You are a concise, helpful assistant.")
    print("Streaming chat CLI. Type 'exit' to quit.")
    while True:
        user_input = input("\nyou> ")
        if user_input.strip().lower() in {"exit", "quit"}:
            break
        print("assistant> ", end="")
        session.send(user_input)


if __name__ == "__main__":
    run_cli()
