# 17 — Guardrails & Security — Advanced / Senior

**Concepts**: red-teaming your own system systematically (structured adversarial testing, not ad hoc), designing defense-in-depth (multiple guardrail layers, not one filter), rate limiting and abuse detection, secure tool-execution sandboxing for agents (least-privilege tool permissions), data governance for RAG systems with sensitive documents (access control at retrieval time, not just at the UI layer).

**Resources**:
- [Anthropic — frontier model security practices](https://www.anthropic.com/news/frontier-model-security)
- OWASP LLM Top 10 — deep dive per category

**Code** (`code/17-guardrails-security/03-advanced/`):
- `red_team_harness.py` — systematic adversarial test suite against the capstone system (injection attempts, jailbreak attempts, PII extraction attempts) with pass/fail reporting
- `access_controlled_rag.py` — retrieval that respects per-user document permissions at the query/index level, not just filtered after the fact

**Interview questions**:
- You're building RAG over a document store where different users have different access permissions. How do you prevent the retrieval step itself from leaking unauthorized content into an answer? (Permission filtering must happen at retrieval/query time via metadata filtering tied to user identity — never filter only at the final answer stage, since the model has already "seen" the unauthorized content by then.)
