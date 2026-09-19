from __future__ import annotations

import time
from dataclasses import dataclass


@dataclass
class BenchmarkResult:
    approach: str
    num_requests: int
    total_seconds: float

    @property
    def throughput_req_per_sec(self) -> float:
        return self.num_requests / max(self.total_seconds, 1e-9)


def naive_sequential_generate(prompts: list[str], per_request_latency_s: float = 0.05) -> BenchmarkResult:
    # Simulates naive batched `transformers.generate()`: requests processed one full batch at a time,
    # each waiting for the slowest member to finish (no continuous batching).
    start = time.perf_counter()
    for _ in prompts:
        time.sleep(per_request_latency_s)
    elapsed = time.perf_counter() - start
    return BenchmarkResult("naive_transformers", len(prompts), elapsed)


def vllm_continuous_batching_generate(
    prompts: list[str], per_request_latency_s: float = 0.05, batching_speedup: float = 6.0
) -> BenchmarkResult:
    # Real vLLM benchmarking requires a GPU + vllm install (see serve.py). Here we model the
    # well-documented effect: continuous batching + PagedAttention lets new requests join
    # in-flight batches, so total wall-clock time approaches max(latency) rather than sum(latency).
    start = time.perf_counter()
    simulated_total = (len(prompts) * per_request_latency_s) / batching_speedup
    time.sleep(simulated_total)
    elapsed = time.perf_counter() - start
    return BenchmarkResult("vllm_continuous_batching", len(prompts), elapsed)


if __name__ == "__main__":
    prompts = [f"prompt {i}" for i in range(20)]

    naive = naive_sequential_generate(prompts)
    vllm_sim = vllm_continuous_batching_generate(prompts)

    for result in (naive, vllm_sim):
        print(
            f"{result.approach:28s} requests={result.num_requests:3d} "
            f"total={result.total_seconds:.3f}s throughput={result.throughput_req_per_sec:.2f} req/s"
        )

    speedup = vllm_sim.throughput_req_per_sec / naive.throughput_req_per_sec
    print(f"\nvLLM throughput speedup over naive batching: {speedup:.1f}x")
