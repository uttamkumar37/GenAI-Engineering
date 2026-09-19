# 10 — Agents — Intermediate

**Concepts**: multi-tool agents, planning (decompose task into subtasks before acting), memory (short-term conversation buffer vs long-term retrieval-based memory), LangGraph basics (nodes, edges, state), simple multi-agent handoff (one agent delegates to another).

**Resources**:
- LangGraph — Quickstart (verify current API — this framework changes fast)
- Anthropic — Building Effective Agents, "workflows vs agents" section

**Code** (`code/10-agents/02-intermediate/`):
- `langgraph_multi_tool_agent/` — agent with 3+ tools, explicit planning step before execution
- `agent_with_memory.py` — long-running conversation where agent retrieves relevant past interactions (reuses the Topic 07/08 RAG pipeline as memory backend)

**Interview questions**:
- What's the difference between a "workflow" and an "agent" in Anthropic's own framing? (Workflows: predefined code paths orchestrating LLM calls. Agents: the LLM dynamically decides its own path/tool sequence. Know when each is appropriate — workflows are more reliable/debuggable.)
