# 18 — LLMOps — Advanced / Senior

**Concepts**: full production observability stack (tracing + cost dashboards + quality-score trends over time, tied to the Topic 16 eval pipeline), alerting on cost/latency/error-rate anomalies, A/B testing prompt or model changes in production safely, multi-region/multi-provider failover architecture, capacity planning for LLM-heavy workloads.

**Resources**:
- [Langfuse — Dashboards & Analytics](https://langfuse.com/docs/analytics) (this category moves fast — search current best practices)

**Code** (`code/18-llmops/03-advanced/`):
- `llmops_full_stack/` — integrate tracing (Langfuse), semantic caching, streaming, fallback chains, and cost/quality dashboards into one cohesive service wrapping the capstone system
- `ab_test_prompt_variants_prod.py` — safely route a % of production traffic to a new prompt/model variant, compare eval scores

**Interview questions**:
- Design the full observability stack you'd want in place before putting an agentic RAG system in front of real users. (Tracing every span, cost-per-request tracking, quality score sampling tied to eval rubrics, alerting thresholds, and a rollback mechanism for prompt/model changes — walk through it as a system, not a tool list.)
