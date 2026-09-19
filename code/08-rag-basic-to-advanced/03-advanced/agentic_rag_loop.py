# requires ANTHROPIC_API_KEY for AnthropicAgentLLM; FakeAgentLLM needs nothing
from __future__ import annotations

import hashlib
import json
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass

MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-opus-5")
EMBEDDING_DIM = 16

DOCUMENTS = [
    "Acme Corp's Q1 revenue was $4.2M, up 10% year over year.",
    "Acme Corp's Q2 revenue was $4.8M, driven by new enterprise contracts.",
    "Operating costs rose in Q2 due to increased cloud infrastructure spend.",
    "The board approved a new pricing tier for enterprise customers in March.",
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


@dataclass
class AgentDecision:
    action: str  # "retrieve" | "answer"
    query: str | None
    answer: str | None


class AgentLLM(ABC):
    @abstractmethod
    def decide(self, question: str, retrieved_so_far: list[str]) -> AgentDecision: ...


class AnthropicAgentLLM(AgentLLM):
    def __init__(self, model: str = MODEL) -> None:
        import anthropic

        self.model = model
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    def decide(self, question: str, retrieved_so_far: list[str]) -> AgentDecision:
        context = "\n".join(f"- {c}" for c in retrieved_so_far) or "(nothing retrieved yet)"
        prompt = (
            f"Question: {question}\n\nRetrieved so far:\n{context}\n\n"
            'Decide whether you have enough context to answer. Reply with JSON only: '
            '{"action": "retrieve", "query": "<refined search query>"} to search again, or '
            '{"action": "answer", "answer": "<final answer>"} if you can answer now.'
        )
        response = self.client.messages.create(
            model=self.model,
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
            output_config={
                "format": {
                    "type": "json_schema",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "action": {"type": "string", "enum": ["retrieve", "answer"]},
                            "query": {"type": "string"},
                            "answer": {"type": "string"},
                        },
                        "required": ["action"],
                        "additionalProperties": False,
                    },
                }
            },
        )
        raw = next(b.text for b in response.content if b.type == "text")
        data = json.loads(raw)
        return AgentDecision(action=data["action"], query=data.get("query"), answer=data.get("answer"))


class FakeAgentLLM(AgentLLM):
    # deterministic 2-step plan: broaden the query once, then answer from what's retrieved
    def decide(self, question: str, retrieved_so_far: list[str]) -> AgentDecision:
        if not retrieved_so_far:
            return AgentDecision(action="retrieve", query=question, answer=None)
        if len(retrieved_so_far) < 3 and "q2" not in " ".join(retrieved_so_far).lower():
            return AgentDecision(action="retrieve", query="Q2 revenue and costs", answer=None)
        answer = "Combining retrieved facts: " + " ".join(retrieved_so_far)
        return AgentDecision(action="answer", query=None, answer=answer)


def agentic_rag(llm: AgentLLM, question: str, max_iterations: int = 4) -> str:
    retrieved: list[str] = []
    for _ in range(max_iterations):
        decision = llm.decide(question, retrieved)
        if decision.action == "answer":
            return decision.answer or ""
        new_chunks = retrieve(decision.query or question)
        for chunk in new_chunks:
            if chunk not in retrieved:
                retrieved.append(chunk)
    return "Could not converge on an answer within the iteration budget."


if __name__ == "__main__":
    llm: AgentLLM = AnthropicAgentLLM() if os.environ.get("ANTHROPIC_API_KEY") else FakeAgentLLM()
    print(agentic_rag(llm, "How did Acme Corp's revenue and costs change between Q1 and Q2?"))
