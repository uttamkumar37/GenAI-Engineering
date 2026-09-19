from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ServingOption:
    name: str
    cost_per_1k_tokens_usd: float
    p50_latency_ms: float
    p95_latency_ms: float
    fixed_monthly_cost_usd: float  # GPU/infra cost that's ~independent of volume, 0 for managed APIs


# Synthetic/hardcoded reference figures (order-of-magnitude realistic as of late 2025) so the
# dashboard is demonstrable without a live GPU or managed-API account.
SERVING_OPTIONS: list[ServingOption] = [
    ServingOption(
        name="managed_api",
        cost_per_1k_tokens_usd=0.0150,
        p50_latency_ms=350,
        p95_latency_ms=900,
        fixed_monthly_cost_usd=0.0,
    ),
    ServingOption(
        name="self_hosted_vllm_fp16",
        cost_per_1k_tokens_usd=0.0040,
        p50_latency_ms=220,
        p95_latency_ms=520,
        fixed_monthly_cost_usd=1800.0,  # single A100 80GB on-demand, amortized monthly
    ),
    ServingOption(
        name="self_hosted_vllm_int4",
        cost_per_1k_tokens_usd=0.0022,
        p50_latency_ms=170,
        p95_latency_ms=410,
        fixed_monthly_cost_usd=900.0,  # smaller/cheaper GPU sufficient for a quantized model
    ),
]
