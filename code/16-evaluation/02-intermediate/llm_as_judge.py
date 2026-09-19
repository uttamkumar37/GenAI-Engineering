from __future__ import annotations

import json
import re
from dataclasses import dataclass


class FakeJudgeLLM:
    """Deterministic mock standing in for a real judge-model API call (no network access here).
    Scores are computed with simple heuristics so the rubric-application logic is real and testable."""

    def complete(self, prompt: str) -> str:
        question_match = re.search(r"Question: (.*)", prompt)
        answer_match = re.search(r"Answer: (.*)", prompt)
        context_match = re.search(r"Context: (.*)", prompt)
        question = question_match.group(1) if question_match else ""
        answer = answer_match.group(1) if answer_match else ""
        context = context_match.group(1) if context_match else ""

        answer_words = set(answer.lower().split())
        context_words = set(context.lower().split())
        question_words = set(question.lower().split())

        grounding = len(answer_words & context_words) / max(len(answer_words), 1)
        relevance = len(answer_words & question_words) / max(len(question_words), 1)
        conciseness = 1.0 if len(answer.split()) <= 40 else 0.5

        overall = round((grounding * 0.5 + relevance * 0.3 + conciseness * 0.2) * 5, 1)
        verdict = {
            "grounding": round(grounding, 2),
            "relevance": round(relevance, 2),
            "conciseness": conciseness,
            "overall_score": overall,
            "rationale": (
                f"Answer shares {len(answer_words & context_words)} content words with the "
                f"provided context and {len(answer_words & question_words)} with the question."
            ),
        }
        return json.dumps(verdict)


JUDGE_PROMPT_TEMPLATE = """You are grading a RAG system's answer against a rubric.
Score grounding (is the answer supported by the context?), relevance (does it
answer the question?), and conciseness. Return JSON with keys: grounding,
relevance, conciseness, overall_score (0-5), rationale.

Question: {question}
Context: {context}
Answer: {answer}
"""


@dataclass
class JudgeVerdict:
    grounding: float
    relevance: float
    conciseness: float
    overall_score: float
    rationale: str


def judge_answer(judge: FakeJudgeLLM, question: str, context: str, answer: str) -> JudgeVerdict:
    prompt = JUDGE_PROMPT_TEMPLATE.format(question=question, context=context, answer=answer)
    raw = judge.complete(prompt)
    data = json.loads(raw)
    return JudgeVerdict(**data)


EVAL_SAMPLES = [
    {
        "question": "What does vLLM use for efficient serving?",
        "context": "vLLM uses continuous batching and PagedAttention to serve LLMs efficiently.",
        "answer": "vLLM uses continuous batching and PagedAttention for efficient serving.",
    },
    {
        "question": "What does vLLM use for efficient serving?",
        "context": "vLLM uses continuous batching and PagedAttention to serve LLMs efficiently.",
        "answer": "I think vLLM is basically like a database index for tokens or something.",
    },
]


if __name__ == "__main__":
    judge = FakeJudgeLLM()
    for sample in EVAL_SAMPLES:
        verdict = judge_answer(judge, **sample)
        print(f"Q: {sample['question']}")
        print(f"A: {sample['answer']}")
        print(
            f"  grounding={verdict.grounding} relevance={verdict.relevance} "
            f"conciseness={verdict.conciseness} overall={verdict.overall_score}/5"
        )
        print(f"  rationale: {verdict.rationale}\n")
