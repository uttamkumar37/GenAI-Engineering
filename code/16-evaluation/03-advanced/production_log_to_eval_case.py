from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class ProductionLogEntry:
    question: str
    answer: str
    contexts: list[str]
    user_thumbs_down: bool
    judge_score: float | None  # 0-5, from an online LLM-judge sample, if scored


@dataclass
class MinedEvalCase:
    question: str
    answer_at_capture_time: str
    contexts: list[str]
    reason_flagged: str
    must_include: list[str]


# Synthetic production log — in a real system this would be pulled from your logging store
# (see topic 18's basic_llm_logging.py) filtered to a recent time window.
SAMPLE_PRODUCTION_LOGS: list[ProductionLogEntry] = [
    ProductionLogEntry(
        question="What does vLLM use for efficient serving?",
        answer="vLLM uses continuous batching and PagedAttention for efficient serving.",
        contexts=["vLLM uses continuous batching and PagedAttention to serve LLMs efficiently."],
        user_thumbs_down=False,
        judge_score=4.5,
    ),
    ProductionLogEntry(
        question="How much does self-hosting save vs a managed API?",
        answer="Self-hosting is always cheaper, no matter the volume.",
        contexts=["Self-hosting becomes cheaper than a managed API only above a certain volume."],
        user_thumbs_down=True,
        judge_score=1.2,
    ),
    ProductionLogEntry(
        question="What is context precision in RAGAS?",
        answer="It measures how many retrieved chunks are actually relevant to the ground truth.",
        contexts=["Context precision measures the proportion of retrieved contexts that are relevant."],
        user_thumbs_down=False,
        judge_score=2.9,
    ),
]

LOW_SCORE_THRESHOLD = 3.0


def _content_words(text: str, min_len: int = 4) -> list[str]:
    return [w.strip(".,!?").lower() for w in text.split() if len(w.strip(".,!?")) >= min_len]


def mine_eval_cases(
    logs: list[ProductionLogEntry], low_score_threshold: float = LOW_SCORE_THRESHOLD
) -> list[MinedEvalCase]:
    mined = []
    for entry in logs:
        flagged_reasons = []
        if entry.user_thumbs_down:
            flagged_reasons.append("user_thumbs_down")
        if entry.judge_score is not None and entry.judge_score < low_score_threshold:
            flagged_reasons.append(f"low_judge_score({entry.judge_score})")

        if not flagged_reasons:
            continue

        # Derive expected-content assertions from the retrieved context (ground truth proxy),
        # not from the (possibly wrong) production answer — that's the whole point of mining failures.
        must_include = _content_words(" ".join(entry.contexts))[:3]

        mined.append(
            MinedEvalCase(
                question=entry.question,
                answer_at_capture_time=entry.answer,
                contexts=entry.contexts,
                reason_flagged=", ".join(flagged_reasons),
                must_include=must_include,
            )
        )
    return mined


def write_eval_cases(cases: list[MinedEvalCase], out_path: Path) -> None:
    out_path.write_text(json.dumps([asdict(c) for c in cases], indent=2))


if __name__ == "__main__":
    mined_cases = mine_eval_cases(SAMPLE_PRODUCTION_LOGS)
    print(f"Mined {len(mined_cases)} new eval case(s) from {len(SAMPLE_PRODUCTION_LOGS)} log entries:\n")
    for case in mined_cases:
        print(f"  question: {case.question}")
        print(f"  flagged because: {case.reason_flagged}")
        print(f"  must_include (from context): {case.must_include}\n")

    out_file = Path(__file__).with_name("mined_eval_cases.json")
    write_eval_cases(mined_cases, out_file)
    print(f"Wrote mined cases to {out_file}")
