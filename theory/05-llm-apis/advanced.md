# 05 — LLM APIs — Advanced / Senior

**Concepts**: unified multi-provider abstraction (reusing Topic 01's `LLMProvider` interface with real APIs), retry/backoff strategies per provider's rate-limit behavior, token counting and cost estimation pre-call, prompt caching (provider-specific, e.g. Anthropic prompt caching) for cost/latency reduction, handling provider outages with fallback chains.

**Resources**:
- [Anthropic — Prompt Caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [Anthropic — Rate Limits](https://docs.anthropic.com/en/api/rate-limits)

**Code** (`code/05-llm-apis/03-advanced/`):
- `unified_llm_gateway/` — provider abstraction (real APIs), automatic retry with exponential backoff, token/cost estimator, prompt-cache-aware request builder, fallback chain (Claude → OpenAI → local Ollama on failure)

**Interview questions**:
- Design a gateway that routes to the cheapest provider that meets a latency SLA, with automatic fallback on failure. (Real system-design interview question for GenAI roles — practice saying it out loud.)
