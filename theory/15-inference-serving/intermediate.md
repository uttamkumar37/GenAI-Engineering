# 15 — Inference & Serving — Intermediate

**Concepts**: vLLM basics (continuous batching, PagedAttention conceptually), quantization (int8/int4, quality/speed tradeoff), throughput vs latency tradeoffs, serving via a simple API wrapper around vLLM.

**Resources**:
- [vLLM — Quickstart](https://docs.vllm.ai/en/latest/getting_started/quickstart.html)
- [Hugging Face — Quantization overview](https://huggingface.co/docs/transformers/quantization/overview)

**Code** (`code/15-inference-serving/02-intermediate/`):
- `vllm_serve_local_model/` — serve a small open model via vLLM, benchmark throughput vs the naive `transformers` approach from fresher level
- `quantization_tradeoff_demo.py` — same model at fp16 vs int8 vs int4, compare speed and a quality metric

**Interview questions**:
- Why does vLLM achieve much higher throughput than naive batched generation? (Continuous batching — new requests join in-flight batches instead of waiting for the whole batch to finish; PagedAttention manages KV cache memory efficiently, connecting back to Topic 04.)
