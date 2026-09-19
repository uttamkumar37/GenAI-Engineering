from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "01-fresher"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "02-intermediate"))

from llm_as_judge import EVAL_SAMPLES, FakeJudgeLLM, judge_answer  # noqa: E402
from ragas_eval_rag import SAMPLES as RAGAS_SAMPLES  # noqa: E402
from ragas_eval_rag import run_fallback_eval  # noqa: E402
from simple_eval_harness import EVAL_CASES, run_suite  # noqa: E402

SCORES_HISTORY_PATH = Path(__file__).with_name("scores_history.json")

# Below-this-score is a regression; tune per project. Kept low here since the mock
# retrieval/judge in this repo are intentionally simplistic (see topic 16 fresher/intermediate files).
THRESHOLDS = {
    "rule_based_pass_rate": 0.6,
    "judge_overall_avg": 2.0,
    "ragas_faithfulness_avg": 0.3,
}


@dataclass
class SuiteScores:
    rule_based_pass_rate: float
    judge_overall_avg: float
    ragas_faithfulness_avg: float


def compute_scores() -> SuiteScores:
    rule_results = run_suite(EVAL_CASES)
    rule_pass_rate = sum(r.passed for r in rule_results) / len(rule_results)

    judge = FakeJudgeLLM()
    judge_scores = [judge_answer(judge, **sample).overall_score for sample in EVAL_SAMPLES]
    judge_avg = sum(judge_scores) / len(judge_scores)

    ragas_rows = run_fallback_eval(RAGAS_SAMPLES)
    faithfulness_avg = sum(row["faithfulness"] for row in ragas_rows) / len(ragas_rows)

    return SuiteScores(
        rule_based_pass_rate=round(rule_pass_rate, 3),
        judge_overall_avg=round(judge_avg, 3),
        ragas_faithfulness_avg=round(faithfulness_avg, 3),
    )


def check_regression(scores: SuiteScores) -> list[str]:
    failures = []
    if scores.rule_based_pass_rate < THRESHOLDS["rule_based_pass_rate"]:
        failures.append(
            f"rule_based_pass_rate {scores.rule_based_pass_rate} < {THRESHOLDS['rule_based_pass_rate']}"
        )
    if scores.judge_overall_avg < THRESHOLDS["judge_overall_avg"]:
        failures.append(f"judge_overall_avg {scores.judge_overall_avg} < {THRESHOLDS['judge_overall_avg']}")
    if scores.ragas_faithfulness_avg < THRESHOLDS["ragas_faithfulness_avg"]:
        failures.append(
            f"ragas_faithfulness_avg {scores.ragas_faithfulness_avg} < {THRESHOLDS['ragas_faithfulness_avg']}"
        )
    return failures


def save_history(scores: SuiteScores) -> None:
    history = []
    if SCORES_HISTORY_PATH.exists():
        history = json.loads(SCORES_HISTORY_PATH.read_text())
    history.append(asdict(scores))
    SCORES_HISTORY_PATH.write_text(json.dumps(history, indent=2))


if __name__ == "__main__":
    scores = compute_scores()
    print("Eval suite scores:")
    for key, value in asdict(scores).items():
        print(f"  {key}: {value}")

    save_history(scores)

    failures = check_regression(scores)
    if failures:
        print("\nREGRESSION DETECTED:")
        for failure in failures:
            print(f"  - {failure}")
        sys.exit(1)

    print("\nAll thresholds met.")
    sys.exit(0)
