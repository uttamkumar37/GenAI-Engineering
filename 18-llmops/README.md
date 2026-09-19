# 18 — LLMOps

## Fresher

**Concepts**: what observability means for LLM apps beyond normal app logging (prompts, completions, token usage, latency per call), basic structured logging of LLM calls.

**Resources**:
- [Langfuse — Get Started](https://langfuse.com/docs/get-started)

**Code** (`code/01-fresher/`):
- `basic_llm_logging.py` — log every LLM call (prompt, response, tokens, latency, cost) to a structured log file

**Interview questions**:
- Why isn't standard APM (application performance monitoring) tooling sufficient for LLM applications? (Doesn't capture prompt/completion content, token economics, or non-deterministic quality drift — needs LLM-specific tracing.)

## Intermediate

**Concepts**: full tracing with Langfuse or OpenTelemetry (nested spans for multi-step agent/RAG pipelines), response caching (semantic + exact-match caching to cut cost/latency), streaming implementation details in production, rate limiting your own API layer, basic fallback chains (already built in Topic 05, now wire into full observability).

**Resources**:
- [Langfuse — Tracing docs](https://langfuse.com/docs/tracing)
- [OpenTelemetry — Python getting started](https://opentelemetry.io/docs/languages/python/getting-started/)

**Code** (`code/02-intermediate/`):
- `langfuse_traced_rag/` — wire full tracing into the Topic 08 RAG pipeline (retrieval span, generation span, total cost/latency)
- `semantic_cache.py` — cache LLM responses keyed by embedding similarity of the prompt, not just exact string match

**Interview questions**:
- How does semantic caching reduce cost, and what's the risk of using it too aggressively? (Cuts redundant LLM calls for similar-but-not-identical queries; risk is returning stale or subtly wrong cached answers for queries that are similar but require different answers — needs a similarity threshold tuned carefully.)

## Advanced / Senior

**Concepts**: full production observability stack (tracing + cost dashboards + quality-score trends over time, tied to the Topic 16 eval pipeline), alerting on cost/latency/error-rate anomalies, A/B testing prompt or model changes in production safely, multi-region/multi-provider failover architecture, capacity planning for LLM-heavy workloads.

**Resources**:
- [Langfuse — Dashboards & Analytics](https://langfuse.com/docs/analytics) (this category moves fast — search current best practices)

**Code** (`code/03-advanced/`):
- `llmops_full_stack/` — integrate tracing (Langfuse), semantic caching, streaming, fallback chains, and cost/quality dashboards into one cohesive service wrapping the capstone system
- `ab_test_prompt_variants_prod.py` — safely route a % of production traffic to a new prompt/model variant, compare eval scores

**Interview questions**:
- Design the full observability stack you'd want in place before putting an agentic RAG system in front of real users. (Tracing every span, cost-per-request tracking, quality score sampling tied to eval rubrics, alerting thresholds, and a rollback mechanism for prompt/model changes — walk through it as a system, not a tool list.)

## Milestone

The capstone system now has full tracing, caching, and a cost/quality dashboard — this satisfies the "cost/latency dashboard" requirement of the final capstone directly.
