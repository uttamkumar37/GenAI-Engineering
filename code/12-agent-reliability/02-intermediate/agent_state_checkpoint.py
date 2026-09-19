from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field


@dataclass
class AgentState:
    task: str
    completed_steps: list[str] = field(default_factory=list)
    remaining_steps: list[str] = field(default_factory=list)
    results: dict[str, str] = field(default_factory=dict)


class CheckpointStore:
    def __init__(self, path: str) -> None:
        self.path = path

    def save(self, state: AgentState) -> None:
        with open(self.path, "w") as f:
            json.dump(asdict(state), f, indent=2)

    def load(self) -> AgentState | None:
        if not os.path.exists(self.path):
            return None
        with open(self.path) as f:
            data = json.load(f)
        return AgentState(**data)

    def clear(self) -> None:
        if os.path.exists(self.path):
            os.remove(self.path)


def execute_step(step: str) -> str:
    return f"result-of({step})"


def run_agent(task: str, all_steps: list[str], store: CheckpointStore, crash_after: int | None = None) -> AgentState:
    state = store.load()
    if state is None:
        state = AgentState(task=task, remaining_steps=list(all_steps))
        print("Starting fresh run.")
    else:
        print(f"Resuming from checkpoint: {len(state.completed_steps)} step(s) already done.")

    steps_run_this_call = 0
    while state.remaining_steps:
        step = state.remaining_steps[0]
        result = execute_step(step)
        state.results[step] = result
        state.completed_steps.append(step)
        state.remaining_steps.pop(0)
        store.save(state)
        steps_run_this_call += 1
        print(f"  completed '{step}' -> {result}")

        if crash_after is not None and steps_run_this_call >= crash_after:
            print("  simulated crash!")
            raise RuntimeError("simulated crash mid-task")

    return state


if __name__ == "__main__":
    checkpoint_path = os.path.join(os.path.dirname(__file__), "_agent_checkpoint.json")
    store = CheckpointStore(checkpoint_path)
    store.clear()

    steps = ["fetch_data", "clean_data", "analyze", "generate_report"]

    try:
        run_agent("build quarterly report", steps, store, crash_after=2)
    except RuntimeError as exc:
        print(f"Run interrupted: {exc}")

    print("\nRestarting agent process after crash...\n")
    final_state = run_agent("build quarterly report", steps, store)
    print("\nFinal state:", final_state)
    store.clear()
