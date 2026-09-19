from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class FakeLLM:
    # deterministic canned responses keyed by simple substring matching, no network calls
    call_count: int = 0

    def complete(self, messages: list[dict[str, str]]) -> str:
        self.call_count += 1
        last_user = messages[-1]["content"]

        if "Observation" not in last_user:
            match = re.search(r"[-+*/() \d.]{3,}", last_user)
            if match:
                expr = match.group(0).strip()
                return f"Thought: I need to compute {expr}.\nAction: calculator[{expr}]"
            return "Thought: I don't see a math expression.\nFinal Answer: I could not find an expression to evaluate."

        obs_match = re.search(r"Observation: (.+)$", last_user, re.MULTILINE)
        result = obs_match.group(1) if obs_match else "unknown"
        return f"Thought: The calculator returned {result}.\nFinal Answer: {result}"


def calculator_tool(expression: str) -> str:
    allowed = set("0123456789.+-*/() ")
    if not set(expression) <= allowed:
        return "error: invalid characters in expression"
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as exc:
        return f"error: {exc}"


ACTION_RE = re.compile(r"Action:\s*calculator\[(.+?)\]")
FINAL_RE = re.compile(r"Final Answer:\s*(.+)")


def run_react_agent(question: str, llm: FakeLLM, max_iterations: int = 5) -> str:
    messages = [{"role": "user", "content": question}]
    scratchpad = question

    for step in range(max_iterations):
        response = llm.complete([{"role": "user", "content": scratchpad}])

        final_match = FINAL_RE.search(response)
        if final_match:
            return final_match.group(1).strip()

        action_match = ACTION_RE.search(response)
        if not action_match:
            return "Agent stalled: no action or final answer produced."

        expression = action_match.group(1)
        observation = calculator_tool(expression)
        scratchpad = f"{scratchpad}\n{response}\nObservation: {observation}"

    return "Agent stopped: reached max iteration cap without a final answer."


if __name__ == "__main__":
    llm = FakeLLM()
    answer = run_react_agent("What is 12 * (3 + 4)?", llm)
    print(f"Answer: {answer}")
    print(f"LLM calls used: {llm.call_count}")

    llm2 = FakeLLM()
    answer2 = run_react_agent("Tell me a joke.", llm2)
    print(f"Answer: {answer2}")
