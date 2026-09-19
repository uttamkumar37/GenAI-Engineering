# 15 — Inference & Serving

## Fresher

**Concepts**: what "serving" means beyond calling an API (hosting your own model), basic latency/throughput vocabulary, batching intuition.

**Resources**:
- [Hugging Face — Text Generation Inference (TGI) overview](https://huggingface.co/docs/text-generation-inference/index)

**Code** (`code/01-fresher/`):
- `local_inference_basic.py` — run a small open model locally with `transformers` `generate()`, measure latency per token

**Interview questions**:
- Why is serving an LLM fundamentally different from serving a typical REST API? (Stateful decoding, GPU memory constraints, variable-length outputs, batching complexity vs typical stateless request/response.)

## Intermediate

**Concepts**: vLLM basics (continuous batching, PagedAttention conceptually), quantization (int8/int4, quality/speed tradeoff), throughput vs latency tradeoffs, serving via a simple API wrapper around vLLM.

**Resources**:
- [vLLM — Quickstart](https://docs.vllm.ai/en/latest/getting_started/quickstart.html)
- [Hugging Face — Quantization overview](https://huggingface.co/docs/transformers/quantization/overview)

**Code** (`code/02-intermediate/`):
- `vllm_serve_local_model/` — serve a small open model via vLLM, benchmark throughput vs the naive `transformers` approach from fresher level
- `quantization_tradeoff_demo.py` — same model at fp16 vs int8 vs int4, compare speed and a quality metric

**Interview questions**:
- Why does vLLM achieve much higher throughput than naive batched generation? (Continuous batching — new requests join in-flight batches instead of waiting for the whole batch to finish; PagedAttention manages KV cache memory efficiently, connecting back to Topic 04.)

## Advanced / Senior

**Concepts**: choosing between self-hosted inference and managed APIs (cost-at-scale breakeven analysis), multi-GPU serving concepts, request routing/load balancing across model replicas, cost/latency dashboarding for a serving layer, speculative decoding (conceptual), when quantization degrades quality unacceptably.

**Resources**:
- [vLLM — Production metrics/deployment docs](https://docs.vllm.ai/en/latest/serving/metrics.html) (verify current doc path)
- Search current vLLM/Anyscale cost-analysis posts — this category moves fast

**Code** (`code/03-advanced/`):
- `serving_cost_latency_dashboard/` — dashboard comparing cost-per-1k-tokens and p50/p95 latency across: managed API, self-hosted vLLM fp16, self-hosted vLLM quantized — with a breakeven-volume calculation

**Interview questions**:
- At what request volume does self-hosting become cheaper than a managed API, and what are you NOT accounting for if you only compare per-token cost? (GPU idle cost, ops/maintenance burden, reliability/SLA differences, engineering time — per-token cost alone is a trap.)

## Milestone

The cost/latency dashboard here becomes a direct component of the final capstone's dashboard requirement — build it with reuse in mind.
