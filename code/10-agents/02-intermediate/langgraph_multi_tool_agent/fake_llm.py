from __future__ import annotations

import re


class FakeLLM:
    # deterministic canned responses via keyword matching, stands in for a real chat model

    def plan(self, task: str) -> list[str]:
        subtasks = []
        if re.search(r"\bweather\b", task, re.IGNORECASE):
            subtasks.append("look up the weather")
        if re.search(r"[-+*/() \d.]{3,}", task):
            subtasks.append("do the calculation")
        if re.search(r"\b(what is|explain|tell me about)\b", task, re.IGNORECASE):
            subtasks.append("search for background info")
        return subtasks or ["answer directly"]

    def choose_tool(self, subtask: str, task: str) -> tuple[str, str]:
        if "weather" in subtask:
            city_match = re.search(r"in (\w+)", task, re.IGNORECASE)
            return "weather", city_match.group(1) if city_match else "paris"
        if "calculation" in subtask:
            expr_match = re.search(r"[-+*/() \d.]{3,}", task)
            return "calculator", expr_match.group(0).strip() if expr_match else "0"
        if "search" in subtask:
            return "search", task
        return "none", ""

    def synthesize(self, task: str, observations: list[str]) -> str:
        if not observations:
            return f"I don't have enough tools to answer: {task}"
        return " | ".join(observations)
