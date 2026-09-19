# 17 — Guardrails & Security — Intermediate

**Concepts**: input/output guardrail patterns (classifier-based filtering, allow/deny lists), PII detection and redaction, jailbreak-resistant system prompt design, sandboxing tool execution (limiting what an agent's tools can actually do).

**Resources**:
- Anthropic — Mitigating jailbreaks and prompt injections (verify current path)
- [Microsoft Presidio — PII detection](https://microsoft.github.io/presidio/)

**Code** (`code/17-guardrails-security/02-intermediate/`):
- `pii_redaction_pipeline.py` — detect and redact PII from text before it's sent to an LLM or logged
- `guardrail_input_filter.py` — classify incoming prompts for injection/jailbreak patterns before processing

**Interview questions**:
- Your RAG system ingests user-uploaded documents that get retrieved into other users' prompts. What's the specific injection risk here, and how do you mitigate it? (A malicious document could contain instructions the model follows as if from the system — mitigate with clear delimiter/framing of retrieved content as data-not-instructions, and content scanning on ingestion.)
