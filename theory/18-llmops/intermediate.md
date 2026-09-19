# 18 — LLMOps — Intermediate

**Concepts**: full tracing with Langfuse or OpenTelemetry (nested spans for multi-step agent/RAG pipelines), response caching (semantic + exact-match caching to cut cost/latency), streaming implementation details in production, rate limiting your own API layer, basic fallback chains (already built in Topic 05, now wire into full observability).

**Resources**:
- [Langfuse — Tracing docs](https://langfuse.com/docs/tracing)
- [OpenTelemetry — Python getting started](https://opentelemetry.io/docs/languages/python/getting-started/)

**Code** (`code/18-llmops/02-intermediate/`):
- `langfuse_traced_rag/` — wire full tracing into the Topic 08 RAG pipeline (retrieval span, generation span, total cost/latency)
- `semantic_cache.py` — cache LLM responses keyed by embedding similarity of the prompt, not just exact string match

**Interview questions**:
- How does semantic caching reduce cost, and what's the risk of using it too aggressively? (Cuts redundant LLM calls for similar-but-not-identical queries; risk is returning stale or subtly wrong cached answers for queries that are similar but require different answers — needs a similarity threshold tuned carefully.)
