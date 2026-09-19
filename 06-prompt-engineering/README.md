# 06 — Prompt Engineering

## Fresher

**Concepts**: system prompt vs user prompt, zero-shot vs few-shot, basic prompt structure (role, task, constraints, format).

**Resources**:
- [Anthropic — Prompt Engineering Overview](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)

**Code** (`code/01-fresher/`):
- `prompt_variants.py` — same task, zero-shot vs few-shot vs with-system-prompt, compare outputs

**Interview questions**:
- When does few-shot prompting help vs hurt? (Helps for format/style consistency; hurts when examples bias the model away from edge cases or bloat context unnecessarily.)

## Intermediate

**Concepts**: structured output (JSON mode / schema-constrained generation), tool/function calling (defining tool schemas, parsing tool-call responses, multi-tool selection), chain-of-thought prompting, prompt templates and versioning.

**Resources**:
- [Anthropic — Tool Use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [Anthropic — Increasing output consistency (JSON)](https://docs.anthropic.com/en/docs/build-with-claude/increase-consistency)

**Code** (`code/02-intermediate/`):
- `structured_output_extraction.py` — extract structured data (invoice fields) from unstructured text using JSON schema
- `tool_calling_demo.py` — define 2-3 tools (calculator, weather-mock, search-mock), let the model choose and call them, feed results back

**Interview questions**:
- Walk through the full loop of a tool-calling interaction, including what happens after the tool returns a result. (Model requests tool → you execute → you send tool_result back as a new turn → model continues — this loop IS the foundation of agents.)

## Advanced / Senior

**Concepts**: prompt injection awareness while designing prompts (preview of Topic 17 security), multi-tool orchestration prompting (when the model must chain 2+ tools), prompt compression/context management for long conversations, evaluating prompt variants systematically (not just eyeballing), prompt versioning/rollback in production.

**Resources**:
- [Anthropic — Reducing hallucinations](https://docs.anthropic.com/en/docs/build-with-claude/reduce-hallucinations)
- [Anthropic — Long context tips](https://docs.anthropic.com/en/docs/build-with-claude/long-context-tips)

**Code** (`code/03-advanced/`):
- `prompt_ab_test_harness.py` — run N prompt variants against a fixed eval set, score outputs (preview of Topic 16 eval work), pick a winner systematically
- `multi_tool_chain_demo.py` — task requiring the model to call tool A, use its result to call tool B

**Interview questions**:
- How do you prevent a prompt regression from silently shipping to production? (Versioned prompts + eval set run in CI — direct bridge to Topic 16.)

## Milestone

A small internal "prompt playground" tool (CLI or simple FastAPI+HTML) to test a prompt against multiple providers and see structured-output/tool-calling behavior side by side.
