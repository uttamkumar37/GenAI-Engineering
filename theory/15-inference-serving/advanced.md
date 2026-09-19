# 15 — Inference & Serving — Advanced / Senior

**Concepts**: choosing between self-hosted inference and managed APIs (cost-at-scale breakeven analysis), multi-GPU serving concepts, request routing/load balancing across model replicas, cost/latency dashboarding for a serving layer, speculative decoding (conceptual), when quantization degrades quality unacceptably.

**Resources**:
- [vLLM — Production metrics/deployment docs](https://docs.vllm.ai/en/latest/serving/metrics.html) (verify current doc path)
- Search current vLLM/Anyscale cost-analysis posts — this category moves fast

**Code** (`code/15-inference-serving/03-advanced/`):
- `serving_cost_latency_dashboard/` — dashboard comparing cost-per-1k-tokens and p50/p95 latency across: managed API, self-hosted vLLM fp16, self-hosted vLLM quantized — with a breakeven-volume calculation

**Interview questions**:
- At what request volume does self-hosting become cheaper than a managed API, and what are you NOT accounting for if you only compare per-token cost? (GPU idle cost, ops/maintenance burden, reliability/SLA differences, engineering time — per-token cost alone is a trap.)
