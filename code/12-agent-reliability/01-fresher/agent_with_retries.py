from __future__ import annotations

import random
import re
import time
from dataclasses import dataclass, field


class ToolTimeoutError(Exception):
    pass


class ToolExecutionError(Exception):
    pass


@dataclass
class FlakyCalculatorTool:
    # simulates a tool that intermittently times out or raises, to exercise retry/timeout logic
    failure_rate: float = 0.5
    call_count: int = 0
    seed: int = 1

    def __post_init__(self) -> None:
        self._rng = random.Random(self.seed)

    def call(self, expression: str, simulated_latency: float = 0.0, timeout: float = 1.0) -> str:
        self.call_count += 1
        if simulated_latency > timeout:
            raise ToolTimeoutError(f"tool call exceeded timeout of {timeout}s")

        if self._rng.random() < self.failure_rate:
            raise ToolExecutionError("transient failure in calculator backend")

        try:
            allowed = set("0123456789.+-*/() ")
            if not set(expression) <= allowed:
                raise ValueError("invalid characters in expression")
            return str(eval(expression, {"__builtins__": {}}, {}))
        except Exception as exc:
            raise ToolExecutionError(str(exc)) from exc


def call_with_retries(
    tool: FlakyCalculatorTool,
    expression: str,
    max_retries: int = 3,
    timeout: float = 1.0,
    backoff_seconds: float = 0.0,
) -> str:
    last_error: Exception | None = None
    for attempt in range(1, max_retries + 1):
        try:
            return tool.call(expression, timeout=timeout)
        except (ToolTimeoutError, ToolExecutionError) as exc:
            last_error = exc
            print(f"attempt {attempt}/{max_retries} failed: {exc}")
            if attempt < max_retries and backoff_seconds:
                time.sleep(backoff_seconds)
    raise ToolExecutionError(f"tool call failed after {max_retries} attempts") from last_error


@dataclass
class FakeLLM:
    def complete(self, prompt: str) -> str:
        match = re.search(r"[-+*/() \d.]{3,}", prompt)
        expr = match.group(0).strip() if match else "0"
        return f"Action: calculator[{expr}]"


def run_agent_with_retries(question: str, max_retries: int = 4) -> str:
    llm = FakeLLM()
    tool = FlakyCalculatorTool(failure_rate=0.6)

    response = llm.complete(question)
    action_match = re.search(r"Action:\s*calculator\[(.+?)\]", response)
    if not action_match:
        return "no action produced"

    expression = action_match.group(1)
    try:
        result = call_with_retries(tool, expression, max_retries=max_retries)
        return f"Final Answer: {result} (took {tool.call_count} attempt(s))"
    except ToolExecutionError as exc:
        return f"Agent gave up: {exc}"


if __name__ == "__main__":
    print(run_agent_with_retries("What is 15 * 3?"))
