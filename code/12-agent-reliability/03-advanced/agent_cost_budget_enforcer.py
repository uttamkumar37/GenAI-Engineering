from __future__ import annotations

from dataclasses import dataclass, field


class BudgetExceededError(Exception):
    def __init__(self, message: str, partial_results: list[str]) -> None:
        super().__init__(message)
        self.partial_results = partial_results


@dataclass
class CostBudget:
    max_dollars: float
    spent_dollars: float = 0.0
    max_calls: int = 20
    calls_made: int = 0

    def charge(self, dollars: float) -> None:
        self.calls_made += 1
        self.spent_dollars += dollars

    def exceeded(self) -> bool:
        return self.spent_dollars > self.max_dollars or self.calls_made > self.max_calls


PRICE_PER_CALL_DOLLARS = 0.03


@dataclass
class BudgetedAgentRun:
    task: str
    budget: CostBudget
    partial_results: list[str] = field(default_factory=list)
    stopped_reason: str = ""


def simulate_llm_call(step: str) -> str:
    return f"model output for step '{step}'"


def run_budgeted_agent(task: str, steps: list[str], budget: CostBudget) -> BudgetedAgentRun:
    run = BudgetedAgentRun(task=task, budget=budget)

    for step in steps:
        if budget.exceeded():
            run.stopped_reason = (
                f"budget exceeded before step '{step}': "
                f"${budget.spent_dollars:.2f} spent / {budget.calls_made} calls"
            )
            raise BudgetExceededError(run.stopped_reason, run.partial_results)

        # per-call budget check happens before charging, so we never overshoot mid-call
        projected_spend = budget.spent_dollars + PRICE_PER_CALL_DOLLARS
        if projected_spend > budget.max_dollars:
            run.stopped_reason = f"projected spend ${projected_spend:.2f} would exceed cap ${budget.max_dollars:.2f}"
            raise BudgetExceededError(run.stopped_reason, run.partial_results)

        result = simulate_llm_call(step)
        budget.charge(PRICE_PER_CALL_DOLLARS)
        run.partial_results.append(result)

    run.stopped_reason = "completed within budget"
    return run


if __name__ == "__main__":
    steps = [f"step-{i}" for i in range(10)]

    budget = CostBudget(max_dollars=0.10)  # will only cover ~3 calls
    try:
        run_budgeted_agent("long research task", steps, budget)
    except BudgetExceededError as exc:
        print(f"Hard-stopped: {exc}")
        print(f"Partial results returned ({len(exc.partial_results)}): {exc.partial_results}")

    print(f"\nFinal spend: ${budget.spent_dollars:.2f} across {budget.calls_made} calls")
