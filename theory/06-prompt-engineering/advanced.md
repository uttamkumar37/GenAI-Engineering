# 06 — Prompt Engineering — Advanced / Senior

**Concepts**: prompt injection awareness while designing prompts (preview of Topic 17 security), multi-tool orchestration prompting (when the model must chain 2+ tools), prompt compression/context management for long conversations, evaluating prompt variants systematically (not just eyeballing), prompt versioning/rollback in production.

**Resources**:
- [Anthropic — Reducing hallucinations](https://docs.anthropic.com/en/docs/build-with-claude/reduce-hallucinations)
- [Anthropic — Long context tips](https://docs.anthropic.com/en/docs/build-with-claude/long-context-tips)

**Code** (`code/06-prompt-engineering/03-advanced/`):
- `prompt_ab_test_harness.py` — run N prompt variants against a fixed eval set, score outputs (preview of Topic 16 eval work), pick a winner systematically
- `multi_tool_chain_demo.py` — task requiring the model to call tool A, use its result to call tool B

**Interview questions**:
- How do you prevent a prompt regression from silently shipping to production? (Versioned prompts + eval set run in CI — direct bridge to Topic 16.)
