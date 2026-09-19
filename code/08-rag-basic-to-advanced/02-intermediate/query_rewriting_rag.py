# requires ANTHROPIC_API_KEY for AnthropicLLM; FakeRewriteLLM needs nothing
from __future__ import annotations

import hashlib
import os
from abc import ABC, abstractmethod

MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-opus-5")
EMBEDDING_DIM = 16

DOCUMENTS = [
    "The premium plan costs $19.99/month and includes unlimited storage.",
    "The basic plan costs $4.99/month with 10GB of storage.",
    "You can upgrade your plan anytime from the account settings page.",
    "Downgrading a plan takes effect at the start of the next billing cycle.",
    "Refunds for plan changes are issued only within 7 days of the change.",
]


def fake_embed(text: str) -> list[float]:
    return [
        (hashlib.sha256(f"{text}:{i}".encode()).digest()[0] / 255.0) * 2 - 1
        for i in range(EMBEDDING_DIM)
    ]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0


def retrieve(query: str, top_k: int = 2) -> list[str]:
    query_vec = fake_embed(query)
    scored = [(cosine_similarity(query_vec, fake_embed(doc)), doc) for doc in DOCUMENTS]
    scored.sort(key=lambda t: t[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]


class RewriteLLM(ABC):
    @abstractmethod
    def rewrite(self, history: list[dict], follow_up: str) -> str: ...

    @abstractmethod
    def answer(self, query: str, context_chunks: list[str]) -> str: ...


class AnthropicLLM(RewriteLLM):
    def __init__(self, model: str = MODEL) -> None:
        import anthropic

        self.model = model
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    def rewrite(self, history: list[dict], follow_up: str) -> str:
        transcript = "\n".join(f"{m['role']}: {m['content']}" for m in history)
        prompt = (
            f"Conversation so far:\n{transcript}\n\nFollow-up question: {follow_up}\n\n"
            "Rewrite the follow-up as a standalone question that includes all necessary "
            "context from the conversation. Reply with only the rewritten question."
        )
        response = self.client.messages.create(
            model=self.model, max_tokens=100, messages=[{"role": "user", "content": prompt}]
        )
        return next(b.text for b in response.content if b.type == "text").strip()

    def answer(self, query: str, context_chunks: list[str]) -> str:
        context = "\n".join(f"- {c}" for c in context_chunks)
        prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer concisely using only the context."
        response = self.client.messages.create(
            model=self.model, max_tokens=200, messages=[{"role": "user", "content": prompt}]
        )
        return next(b.text for b in response.content if b.type == "text")


class FakeRewriteLLM(RewriteLLM):
    # deterministic heuristic: splice the previous user turn's subject into the follow-up
    def rewrite(self, history: list[dict], follow_up: str) -> str:
        previous_user_turns = [m["content"] for m in history if m["role"] == "user"]
        if not previous_user_turns:
            return follow_up
        subject = previous_user_turns[-1]
        return f"{follow_up} (regarding: {subject})"

    def answer(self, query: str, context_chunks: list[str]) -> str:
        return f"Based on the retrieved context, here's what applies to '{query}': " + " ".join(
            context_chunks
        )


def conversational_rag(llm: RewriteLLM, history: list[dict], follow_up: str) -> tuple[str, str]:
    standalone_query = llm.rewrite(history, follow_up) if history else follow_up
    chunks = retrieve(standalone_query)
    answer = llm.answer(standalone_query, chunks)
    return standalone_query, answer


if __name__ == "__main__":
    llm: RewriteLLM = AnthropicLLM() if os.environ.get("ANTHROPIC_API_KEY") else FakeRewriteLLM()
    history = [
        {"role": "user", "content": "What does the premium plan cost?"},
        {"role": "assistant", "content": "The premium plan costs $19.99/month with unlimited storage."},
    ]
    follow_up = "Can I get a refund if I switch away from it?"
    rewritten, answer = conversational_rag(llm, history, follow_up)
    print(f"rewritten query: {rewritten}")
    print(f"answer: {answer}")
