# requires a local Ollama server (ollama serve) with a model pulled, e.g. `ollama pull llama3.2`
from __future__ import annotations

import os

import ollama

MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")
HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")


class OllamaChatSession:
    def __init__(self, client: ollama.Client, system: str | None = None) -> None:
        self.client = client
        self.history: list[dict] = []
        if system:
            self.history.append({"role": "system", "content": system})

    def send(self, user_message: str) -> str:
        self.history.append({"role": "user", "content": user_message})
        chunks: list[str] = []
        for part in self.client.chat(model=MODEL, messages=self.history, stream=True):
            text = part["message"]["content"]
            print(text, end="", flush=True)
            chunks.append(text)
        print()
        reply = "".join(chunks)
        self.history.append({"role": "assistant", "content": reply})
        return reply


def run_cli() -> None:
    client = ollama.Client(host=HOST)
    session = OllamaChatSession(client, system="You are a concise, helpful assistant.")
    print(f"Local Ollama chat ({MODEL}). Type 'exit' to quit.")
    while True:
        user_input = input("\nyou> ")
        if user_input.strip().lower() in {"exit", "quit"}:
            break
        print("assistant> ", end="")
        session.send(user_input)


if __name__ == "__main__":
    run_cli()
