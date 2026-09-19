# 12 — Agent Reliability — Fresher

**Concepts**: why agents fail (tool errors, hallucinated tool args, infinite loops), basic retry logic, timeouts per tool call.

**Resources**:
- Anthropic — Building Effective Agents, "reliability" considerations section

**Code** (`code/12-agent-reliability/01-fresher/`):
- `agent_with_retries.py` — wrap tool calls with retry + timeout, add to the Topic 10 basic agent

**Interview questions**:
- What's the difference between retrying a failed LLM call and retrying a failed tool call — should you handle them the same way? (LLM call failure = infra issue, safe to retry as-is; tool call failure might mean the model chose wrong args — retrying identically won't help, may need to re-prompt with the error.)
