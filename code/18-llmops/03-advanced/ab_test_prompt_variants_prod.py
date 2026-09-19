from __future__ import annotations

import hashlib
import statistics
from dataclasses import dataclass, field


@dataclass
class PromptVariant:
    name: str
    system_prompt: str
    traffic_pct: float  # 0-100, must sum to 100 across all variants in a router


class TrafficRouter:
    """Deterministic, sticky routing by hashing a stable user/session id into a bucket —
    avoids random per-request routing so the same user consistently sees the same variant."""

    def __init__(self, variants: list[PromptVariant]) -> None:
        total = sum(v.traffic_pct for v in variants)
        if abs(total - 100.0) > 1e-6:
            raise ValueError(f"traffic_pct must sum to 100, got {total}")
        self._variants = variants

    def assign(self, session_id: str) -> PromptVariant:
        bucket = int(hashlib.sha256(session_id.encode()).hexdigest(), 16) % 100
        cumulative = 0.0
        for variant in self._variants:
            cumulative += variant.traffic_pct
            if bucket < cumulative:
                return variant
        return self._variants[-1]


class FakeLLM:
    """Deterministic mock: variant B is modeled as producing slightly higher-quality,
    slightly slower responses, so the A/B comparison logic has a real signal to detect."""

    def complete(self, variant: PromptVariant, prompt: str) -> tuple[str, float, float]:
        if variant.name == "variant_b":
            response = f"[{variant.name}] Detailed, well-structured answer to: {prompt}"
            quality_score = 4.2
            latency_ms = 340.0
        else:
            response = f"[{variant.name}] {prompt}"
            quality_score = 3.4
            latency_ms = 210.0
        return response, quality_score, latency_ms


@dataclass
class TrialResult:
    session_id: str
    variant_name: str
    quality_score: float
    latency_ms: float


@dataclass
class ABTestReport:
    variant_scores: dict[str, list[float]] = field(default_factory=dict)
    variant_latencies: dict[str, list[float]] = field(default_factory=dict)


def run_ab_test(router: TrafficRouter, llm: FakeLLM, sessions: list[str], prompt: str) -> ABTestReport:
    report = ABTestReport()
    for session_id in sessions:
        variant = router.assign(session_id)
        _, quality, latency = llm.complete(variant, prompt)
        report.variant_scores.setdefault(variant.name, []).append(quality)
        report.variant_latencies.setdefault(variant.name, []).append(latency)
    return report


def summarize(report: ABTestReport) -> dict[str, dict[str, float]]:
    summary = {}
    for name, scores in report.variant_scores.items():
        latencies = report.variant_latencies[name]
        summary[name] = {
            "n": len(scores),
            "avg_quality": round(statistics.mean(scores), 3),
            "stdev_quality": round(statistics.pstdev(scores), 3) if len(scores) > 1 else 0.0,
            "avg_latency_ms": round(statistics.mean(latencies), 2),
        }
    return summary


def is_statistically_meaningful(report: ABTestReport, min_n: int = 30) -> bool:
    # Simple sample-size gate; a real system would run a proper significance test
    # (e.g. Welch's t-test) once both variants have enough samples.
    return all(len(scores) >= min_n for scores in report.variant_scores.values())


if __name__ == "__main__":
    variants = [
        PromptVariant("variant_a_control", "You are a helpful assistant.", traffic_pct=80.0),
        PromptVariant("variant_b", "You are a meticulous, detail-oriented assistant.", traffic_pct=20.0),
    ]
    router = TrafficRouter(variants)
    llm = FakeLLM()

    sessions = [f"user_{i}" for i in range(200)]
    report = run_ab_test(router, llm, sessions, prompt="Explain vector databases.")

    print("A/B test summary:")
    for name, stats in summarize(report).items():
        print(f"  {name}: {stats}")

    print(f"\nSample size sufficient for significance testing: {is_statistically_meaningful(report)}")

    # Sticky routing check: same session always gets the same variant.
    repeat_assignment = [router.assign("user_42").name for _ in range(5)]
    print(f"Sticky routing check for user_42: {repeat_assignment}")
