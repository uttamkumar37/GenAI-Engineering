# 17 — Guardrails & Security

> All techniques here are for defensive/educational use against your own test systems.

## Fresher

**Concepts**: what prompt injection is (basic example), what PII leakage risk looks like, basic input sanitization.

**Resources**:
- [OWASP — Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

**Code** (`code/01-fresher/`):
- `prompt_injection_demo.py` — demonstrate a basic injection attack against an unguarded RAG pipeline (e.g. malicious content in a retrieved document overriding instructions) — defensive/educational purpose only, on your own test system

**Interview questions**:
- What makes prompt injection fundamentally different from traditional injection attacks like SQL injection? (No clean separation between "code" and "data" — the model reads untrusted content as part of its instruction-following context.)

## Intermediate

**Concepts**: input/output guardrail patterns (classifier-based filtering, allow/deny lists), PII detection and redaction, jailbreak-resistant system prompt design, sandboxing tool execution (limiting what an agent's tools can actually do).

**Resources**:
- Anthropic — Mitigating jailbreaks and prompt injections (verify current path)
- [Microsoft Presidio — PII detection](https://microsoft.github.io/presidio/)

**Code** (`code/02-intermediate/`):
- `pii_redaction_pipeline.py` — detect and redact PII from text before it's sent to an LLM or logged
- `guardrail_input_filter.py` — classify incoming prompts for injection/jailbreak patterns before processing

**Interview questions**:
- Your RAG system ingests user-uploaded documents that get retrieved into other users' prompts. What's the specific injection risk here, and how do you mitigate it? (A malicious document could contain instructions the model follows as if from the system — mitigate with clear delimiter/framing of retrieved content as data-not-instructions, and content scanning on ingestion.)

## Advanced / Senior

**Concepts**: red-teaming your own system systematically (structured adversarial testing, not ad hoc), designing defense-in-depth (multiple guardrail layers, not one filter), rate limiting and abuse detection, secure tool-execution sandboxing for agents (least-privilege tool permissions), data governance for RAG systems with sensitive documents (access control at retrieval time, not just at the UI layer).

**Resources**:
- [Anthropic — frontier model security practices](https://www.anthropic.com/news/frontier-model-security)
- OWASP LLM Top 10 — deep dive per category

**Code** (`code/03-advanced/`):
- `red_team_harness.py` — systematic adversarial test suite against the capstone system (injection attempts, jailbreak attempts, PII extraction attempts) with pass/fail reporting
- `access_controlled_rag.py` — retrieval that respects per-user document permissions at the query/index level, not just filtered after the fact

**Interview questions**:
- You're building RAG over a document store where different users have different access permissions. How do you prevent the retrieval step itself from leaking unauthorized content into an answer? (Permission filtering must happen at retrieval/query time via metadata filtering tied to user identity — never filter only at the final answer stage, since the model has already "seen" the unauthorized content by then.)

## Milestone

A red-team report against your own capstone system, with guardrails implemented in response to real findings — shows you think adversarially, not just constructively.
