from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from functools import wraps
from typing import Any, Callable


@dataclass
class TraceEvent:
    event_type: str  # "llm_call" | "tool_call" | "decision" | "error"
    name: str
    input_summary: str
    output_summary: str
    duration_ms: float
    cost_dollars: float = 0.0
    timestamp: float = field(default_factory=time.time)


class AgentTracer:
    def __init__(self, run_id: str) -> None:
        self.run_id = run_id
        self.events: list[TraceEvent] = []

    def record(self, event: TraceEvent) -> None:
        self.events.append(event)

    def total_cost(self) -> float:
        return sum(e.cost_dollars for e in self.events)

    def export(self) -> str:
        return json.dumps(
            {"run_id": self.run_id, "total_cost_dollars": self.total_cost(), "events": [asdict(e) for e in self.events]},
            indent=2,
        )


def traced_call(tracer: AgentTracer, event_type: str, cost_dollars: float = 0.0) -> Callable:
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start = time.perf_counter()
            try:
                result = fn(*args, **kwargs)
                duration_ms = (time.perf_counter() - start) * 1000
                tracer.record(
                    TraceEvent(
                        event_type=event_type,
                        name=fn.__name__,
                        input_summary=str(kwargs or args)[:200],
                        output_summary=str(result)[:200],
                        duration_ms=round(duration_ms, 3),
                        cost_dollars=cost_dollars,
                    )
                )
                return result
            except Exception as exc:
                duration_ms = (time.perf_counter() - start) * 1000
                tracer.record(
                    TraceEvent(
                        event_type="error",
                        name=fn.__name__,
                        input_summary=str(kwargs or args)[:200],
                        output_summary=f"{type(exc).__name__}: {exc}",
                        duration_ms=round(duration_ms, 3),
                    )
                )
                raise

        return wrapper

    return decorator


if __name__ == "__main__":
    tracer = AgentTracer(run_id="run-001")

    @traced_call(tracer, "llm_call", cost_dollars=0.02)
    def call_llm(prompt: str) -> str:
        return f"decided to use calculator for '{prompt}'"

    @traced_call(tracer, "tool_call")
    def calculator(expression: str) -> str:
        return str(eval(expression, {"__builtins__": {}}, {}))

    @traced_call(tracer, "tool_call")
    def flaky_tool() -> str:
        raise ConnectionError("upstream service unavailable")

    call_llm("What is 8 * 9?")
    calculator("8 * 9")
    try:
        flaky_tool()
    except ConnectionError:
        pass

    print(tracer.export())
