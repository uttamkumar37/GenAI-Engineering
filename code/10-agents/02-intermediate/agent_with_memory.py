from __future__ import annotations

# topics 07/08 (embeddings/RAG) code folders are not yet implemented in this repo, so this
# file implements a minimal self-contained keyword-overlap "retrieval memory" store standing
# in for the real embedding-based RAG pipeline described in the theory doc
from dataclasses import dataclass, field


@dataclass
class MemoryStore:
    long_term: list[dict[str, str]] = field(default_factory=list)

    def add(self, role: str, content: str) -> None:
        self.long_term.append({"role": role, "content": content})

    def retrieve(self, query: str, top_k: int = 2) -> list[dict[str, str]]:
        query_words = set(query.lower().split())

        def overlap(entry: dict[str, str]) -> int:
            return len(query_words & set(entry["content"].lower().split()))

        scored = [(overlap(e), e) for e in self.long_term]
        scored = [pair for pair in scored if pair[0] > 0]
        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [entry for _, entry in scored[:top_k]]


class FakeLLM:
    def respond(self, user_input: str, short_term: list[dict[str, str]], retrieved: list[dict[str, str]]) -> str:
        if retrieved:
            memory_snippets = "; ".join(m["content"] for m in retrieved)
            return f"Based on what you told me before ({memory_snippets}), here's my answer to '{user_input}'."
        if "my name is" in user_input.lower():
            name = user_input.lower().split("my name is", 1)[1].strip().rstrip(".")
            return f"Nice to meet you, {name}. I'll remember that."
        return f"I don't have relevant history for '{user_input}' yet."


class ConversationalAgent:
    def __init__(self, short_term_limit: int = 4) -> None:
        self.llm = FakeLLM()
        self.memory = MemoryStore()
        self.short_term: list[dict[str, str]] = []
        self.short_term_limit = short_term_limit

    def turn(self, user_input: str) -> str:
        retrieved = self.memory.retrieve(user_input)
        response = self.llm.respond(user_input, self.short_term, retrieved)

        self.short_term.append({"role": "user", "content": user_input})
        self.short_term.append({"role": "assistant", "content": response})
        self.short_term = self.short_term[-self.short_term_limit :]

        self.memory.add("user", user_input)
        self.memory.add("assistant", response)
        return response


if __name__ == "__main__":
    agent = ConversationalAgent()
    turns = [
        "My name is Priya.",
        "I love hiking in the mountains.",
        "What do you know about my hobbies?",
        "What is my name?",
    ]
    for turn in turns:
        print(f"User: {turn}")
        print(f"Agent: {agent.turn(turn)}\n")
