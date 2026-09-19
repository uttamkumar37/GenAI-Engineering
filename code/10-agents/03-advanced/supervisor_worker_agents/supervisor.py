from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field

from workers import ResearchWorker, WorkerResult


@dataclass
class SupervisorRun:
    task: str
    subtasks: list[str]
    worker_results: list[WorkerResult] = field(default_factory=list)
    final_report: str = ""


class Supervisor:
    MAX_WORKERS = 3

    def decompose(self, task: str) -> list[str]:
        candidate_topics = ["pricing", "features", "market"]
        subtasks = [f"research {topic} for: {task}" for topic in candidate_topics]
        return subtasks[: self.MAX_WORKERS]

    def run(self, task: str) -> SupervisorRun:
        subtasks = self.decompose(task)
        run = SupervisorRun(task=task, subtasks=subtasks)

        # cost-aware: cap concurrent sub-agent spawns at MAX_WORKERS, run them in parallel
        with ThreadPoolExecutor(max_workers=self.MAX_WORKERS) as pool:
            futures = [
                pool.submit(ResearchWorker(f"worker-{i}").run, subtask)
                for i, subtask in enumerate(subtasks)
            ]
            run.worker_results = [f.result() for f in futures]

        run.final_report = self._aggregate(run.worker_results)
        return run

    def _aggregate(self, results: list[WorkerResult]) -> str:
        lines = [f"- ({r.worker_name}) {r.subtask}: {r.output}" for r in results]
        return "Research summary:\n" + "\n".join(lines)


if __name__ == "__main__":
    supervisor = Supervisor()
    run = supervisor.run("evaluate our SaaS competitors")
    print(run.final_report)
    print(f"\nTotal worker tool calls: {sum(len(r.tool_calls) for r in run.worker_results)}")
