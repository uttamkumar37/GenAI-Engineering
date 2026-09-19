# 17 — Guardrails & Security — Fresher

**Concepts**: what prompt injection is (basic example), what PII leakage risk looks like, basic input sanitization.

**Resources**:
- [OWASP — Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

**Code** (`code/17-guardrails-security/01-fresher/`):
- `prompt_injection_demo.py` — demonstrate a basic injection attack against an unguarded RAG pipeline (e.g. malicious content in a retrieved document overriding instructions) — defensive/educational purpose only, on your own test system

**Interview questions**:
- What makes prompt injection fundamentally different from traditional injection attacks like SQL injection? (No clean separation between "code" and "data" — the model reads untrusted content as part of its instruction-following context.)
