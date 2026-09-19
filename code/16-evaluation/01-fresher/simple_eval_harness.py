from __future__ import annotations

from dataclasses import dataclass, field


# Topic 08's RAG pipeline isn't implemented in this repo yet, so this harness ships a small,
# self-contained mock RAG pipeline (retrieval + templated answer) matching the same
# `answer(question) -> str` interface it would expose, so the eval logic is genuinely exercised.
_DOCS = {
    "vllm": "vLLM uses continuous batching and PagedAttention to serve LLMs efficiently.",
    "pii": "PII redaction removes personally identifiable information like emails and phone numbers.",
    "rag": "RAG retrieves relevant documents and passes them to an LLM as context before generation.",
    "quantization": "Quantization reduces model weight precision (fp16 to int8/int4) to save memory.",
}


def mock_retrieve(question: str, k: int = 1) -> list[str]:
    question_lower = question.lower()
    scored = [(sum(word in question_lower for word in doc.lower().split()), doc) for doc in _DOCS.values()]
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [doc for _, doc in scored[:k]]


def mock_rag_answer(question: str) -> str:
    context = mock_retrieve(question, k=1)[0]
    return context  # templated "answer" for this mock is just the retrieved passage


@dataclass
class EvalCase:
    question: str
    must_include: list[str] = field(default_factory=list)  # substrings expected in the answer
    must_not_include: list[str] = field(default_factory=list)


@dataclass
class EvalResult:
    case: EvalCase
    answer: str
    passed: bool
    reasons: list[str]


EVAL_CASES: list[EvalCase] = [
    EvalCase("What does vLLM use for efficient serving?", must_include=["continuous batching"]),
    EvalCase("How does vLLM manage memory?", must_include=["PagedAttention"]),
    EvalCase("What is PII redaction?", must_include=["personally identifiable"]),
    EvalCase("What kind of data does PII redaction remove?", must_include=["emails", "phone numbers"]),
    EvalCase("What does RAG do before generation?", must_include=["retrieves relevant documents"]),
    EvalCase("What context does RAG give the LLM?", must_include=["context"]),
    EvalCase("What is quantization?", must_include=["reduces model weight precision"]),
    EvalCase("Does quantization save memory?", must_include=["save memory"]),
    EvalCase("What precision levels does quantization mention?", must_include=["fp16", "int8", "int4"]),
    EvalCase("Is vLLM related to SQL databases?", must_not_include=["SQL", "database"]),
]


def run_case(case: EvalCase) -> EvalResult:
    answer = mock_rag_answer(case.question)
    reasons: list[str] = []
    passed = True
    for phrase in case.must_include:
        if phrase.lower() not in answer.lower():
            passed = False
            reasons.append(f"missing expected phrase: {phrase!r}")
    for phrase in case.must_not_include:
        if phrase.lower() in answer.lower():
            passed = False
            reasons.append(f"contains forbidden phrase: {phrase!r}")
    return EvalResult(case=case, answer=answer, passed=passed, reasons=reasons)


def run_suite(cases: list[EvalCase]) -> list[EvalResult]:
    return [run_case(case) for case in cases]


if __name__ == "__main__":
    results = run_suite(EVAL_CASES)
    passed_count = sum(r.passed for r in results)

    for i, result in enumerate(results, 1):
        status = "PASS" if result.passed else "FAIL"
        print(f"[{i:2d}] {status}  {result.case.question}")
        if not result.passed:
            for reason in result.reasons:
                print(f"      - {reason}")

    print(f"\n{passed_count}/{len(results)} cases passed")
