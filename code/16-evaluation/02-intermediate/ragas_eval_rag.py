from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RagSample:
    question: str
    answer: str
    contexts: list[str]
    ground_truth: str


SAMPLES: list[RagSample] = [
    RagSample(
        question="What does vLLM use for efficient serving?",
        answer="vLLM uses continuous batching and PagedAttention for efficient serving.",
        contexts=["vLLM uses continuous batching and PagedAttention to serve LLMs efficiently."],
        ground_truth="vLLM uses continuous batching and PagedAttention.",
    ),
    RagSample(
        question="What does quantization reduce?",
        answer="Quantization mostly changes the model's color scheme for better UX.",
        contexts=["Quantization reduces model weight precision (fp16 to int8/int4) to save memory."],
        ground_truth="Quantization reduces model weight precision to save memory.",
    ),
]


# --- Hand-rolled fallback metrics (no external package required) ---------------------


def _tokenize(text: str) -> set[str]:
    return {w.strip(".,!?").lower() for w in text.split() if len(w) > 2}


def simple_faithfulness(answer: str, contexts: list[str]) -> float:
    # Proxy: fraction of the answer's content words that also appear in the retrieved context.
    answer_words = _tokenize(answer)
    context_words = set().union(*(_tokenize(c) for c in contexts)) if contexts else set()
    if not answer_words:
        return 0.0
    return len(answer_words & context_words) / len(answer_words)


def simple_context_precision(contexts: list[str], ground_truth: str) -> float:
    # Proxy: fraction of retrieved contexts that overlap meaningfully with the ground truth.
    truth_words = _tokenize(ground_truth)
    if not contexts:
        return 0.0
    relevant = sum(1 for c in contexts if len(_tokenize(c) & truth_words) / max(len(truth_words), 1) > 0.3)
    return relevant / len(contexts)


def simple_answer_relevancy(answer: str, question: str) -> float:
    answer_words = _tokenize(answer)
    question_words = _tokenize(question)
    if not question_words:
        return 0.0
    return len(answer_words & question_words) / len(question_words)


def run_fallback_eval(samples: list[RagSample]) -> list[dict[str, float]]:
    results = []
    for sample in samples:
        results.append(
            {
                "question": sample.question,
                "faithfulness": round(simple_faithfulness(sample.answer, sample.contexts), 2),
                "context_precision": round(simple_context_precision(sample.contexts, sample.ground_truth), 2),
                "answer_relevancy": round(simple_answer_relevancy(sample.answer, sample.question), 2),
            }
        )
    return results


# --- Real RAGAS integration (requires `pip install ragas datasets`) ------------------
# NOTE ON API UNCERTAINTY: ragas's public API has changed across versions (0.1.x used
# `ragas.evaluate(dataset, metrics=[...])` with a HuggingFace `datasets.Dataset`; newer
# 0.2.x releases reworked metric classes and added a `SingleTurnSample`/`EvaluationDataset`
# abstraction). The code below follows the 0.1.x-style API, which is the version this was
# most confidently seen; verify against your installed `ragas.__version__` before relying on it.


def run_real_ragas_eval(samples: list[RagSample]):
    from datasets import Dataset
    from ragas import evaluate
    from ragas.metrics import answer_relevancy, context_precision, faithfulness

    dataset = Dataset.from_dict(
        {
            "question": [s.question for s in samples],
            "answer": [s.answer for s in samples],
            "contexts": [s.contexts for s in samples],
            "ground_truth": [s.ground_truth for s in samples],
        }
    )
    return evaluate(dataset, metrics=[faithfulness, answer_relevancy, context_precision])


if __name__ == "__main__":
    print("Fallback (hand-rolled, no external deps) RAGAS-style metrics:")
    for row in run_fallback_eval(SAMPLES):
        print(f"  {row}")

    print("\nAttempting real ragas evaluation (requires `pip install ragas datasets` + an LLM key)...")
    try:
        result = run_real_ragas_eval(SAMPLES)
        print(result)
    except ImportError:
        print("  ragas/datasets not installed in this environment — skipped. See run_real_ragas_eval().")
    except Exception as exc:  # ragas needs a real LLM/embeddings client for its judge metrics
        print(f"  real ragas evaluation requires configured LLM/embeddings clients — skipped ({exc!r}).")
