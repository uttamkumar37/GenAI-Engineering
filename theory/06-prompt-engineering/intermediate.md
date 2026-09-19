# 06 — Prompt Engineering — Intermediate

**Concepts**: structured output (JSON mode / schema-constrained generation), tool/function calling (defining tool schemas, parsing tool-call responses, multi-tool selection), chain-of-thought prompting, prompt templates and versioning.

**Resources**:
- [Anthropic — Tool Use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [Anthropic — Increasing output consistency (JSON)](https://docs.anthropic.com/en/docs/build-with-claude/increase-consistency)

**Code** (`code/06-prompt-engineering/02-intermediate/`):
- `structured_output_extraction.py` — extract structured data (invoice fields) from unstructured text using JSON schema
- `tool_calling_demo.py` — define 2-3 tools (calculator, weather-mock, search-mock), let the model choose and call them, feed results back

**Interview questions**:
- Walk through the full loop of a tool-calling interaction, including what happens after the tool returns a result. (Model requests tool → you execute → you send tool_result back as a new turn → model continues — this loop IS the foundation of agents.)
