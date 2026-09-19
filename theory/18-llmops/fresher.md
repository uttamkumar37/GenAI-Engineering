# 18 — LLMOps — Fresher

**Concepts**: what observability means for LLM apps beyond normal app logging (prompts, completions, token usage, latency per call), basic structured logging of LLM calls.

**Resources**:
- [Langfuse — Get Started](https://langfuse.com/docs/get-started)

**Code** (`code/18-llmops/01-fresher/`):
- `basic_llm_logging.py` — log every LLM call (prompt, response, tokens, latency, cost) to a structured log file

**Interview questions**:
- Why isn't standard APM (application performance monitoring) tooling sufficient for LLM applications? (Doesn't capture prompt/completion content, token economics, or non-deterministic quality drift — needs LLM-specific tracing.)
