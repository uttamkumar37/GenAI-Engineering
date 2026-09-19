from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TrajectoryStep:
    tool_name: str
    tool_args: str
    result: str


@dataclass
class Trajectory:
    task: str
    steps: list[TrajectoryStep] = field(default_factory=list)
    final_answer: str = ""

    def log(self, tool_name: str, tool_args: str, result: str) -> None:
        self.steps.append(TrajectoryStep(tool_name, tool_args, result))


@dataclass
class TrajectoryScore:
    redundant_calls: int
    order_penalty: int
    step_count: int
    score: float
    notes: list[str]


EXPECTED_ORDER = ["search", "calculator", "synthesize"]


def score_trajectory(trajectory: Trajectory) -> TrajectoryScore:
    notes: list[str] = []

    seen_calls = [(s.tool_name, s.tool_args) for s in trajectory.steps]
    redundant_calls = len(seen_calls) - len(set(seen_calls))
    if redundant_calls:
        notes.append(f"{redundant_calls} redundant tool call(s) with identical args repeated")

    used_tools = [s.tool_name for s in trajectory.steps if s.tool_name in EXPECTED_ORDER]
    expected_subsequence = [t for t in EXPECTED_ORDER if t in used_tools]
    order_penalty = 0 if used_tools == expected_subsequence else 1
    if order_penalty:
        notes.append(f"tool call order {used_tools} deviates from expected {expected_subsequence}")

    step_count = len(trajectory.steps)
    if step_count > 6:
        notes.append(f"trajectory unusually long ({step_count} steps) — possible inefficiency")

    # simple weighted score: fewer redundant calls and closer-to-expected order score higher
    score = max(0.0, 1.0 - 0.25 * redundant_calls - 0.3 * order_penalty - 0.02 * max(0, step_count - 6))

    return TrajectoryScore(
        redundant_calls=redundant_calls,
        order_penalty=order_penalty,
        step_count=step_count,
        score=round(score, 2),
        notes=notes,
    )


if __name__ == "__main__":
    good = Trajectory(task="Find competitor pricing and compute a 10% discount")
    good.log("search", "competitor pricing", "found: $10-$50/month")
    good.log("calculator", "50 * 0.9", "45")
    good.log("synthesize", "", "Discounted top-tier price is $45/month")

    wasteful = Trajectory(task="Find competitor pricing and compute a 10% discount")
    wasteful.log("search", "competitor pricing", "found: $10-$50/month")
    wasteful.log("search", "competitor pricing", "found: $10-$50/month")
    wasteful.log("calculator", "50 * 0.9", "45")
    wasteful.log("calculator", "50 * 0.9", "45")
    wasteful.log("synthesize", "", "Discounted top-tier price is $45/month")

    for name, traj in [("good", good), ("wasteful", wasteful)]:
        result = score_trajectory(traj)
        print(f"[{name}] score={result.score} redundant={result.redundant_calls} notes={result.notes}")
