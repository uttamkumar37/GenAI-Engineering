from __future__ import annotations

from dataclasses import dataclass


@dataclass
class WorkerResult:
    worker_name: str
    subtask: str
    output: str
    tool_calls: list[str]


class ResearchWorker:
    # simulates a sub-agent doing focused research on one subtopic, using a fake knowledge base

    KNOWLEDGE_BASE = {
        "pricing": "Competitor pricing ranges from $10-$50/month across tiers.",
        "features": "Competitors offer SSO, audit logs, and API access as premium features.",
        "market": "The target market is mid-size B2B SaaS companies with 50-500 employees.",
    }

    def __init__(self, name: str) -> None:
        self.name = name

    def run(self, subtask: str) -> WorkerResult:
        tool_calls = [f"search('{subtask}')"]
        matched = next(
            (v for k, v in self.KNOWLEDGE_BASE.items() if k in subtask.lower()),
            "No specific data found; returning a generic placeholder finding.",
        )
        return WorkerResult(worker_name=self.name, subtask=subtask, output=matched, tool_calls=tool_calls)
