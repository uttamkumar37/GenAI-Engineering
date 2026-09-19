# 15 — Inference & Serving — Fresher

**Concepts**: what "serving" means beyond calling an API (hosting your own model), basic latency/throughput vocabulary, batching intuition.

**Resources**:
- [Hugging Face — Text Generation Inference (TGI) overview](https://huggingface.co/docs/text-generation-inference/index)

**Code** (`code/15-inference-serving/01-fresher/`):
- `local_inference_basic.py` — run a small open model locally with `transformers` `generate()`, measure latency per token

**Interview questions**:
- Why is serving an LLM fundamentally different from serving a typical REST API? (Stateful decoding, GPU memory constraints, variable-length outputs, batching complexity vs typical stateless request/response.)
