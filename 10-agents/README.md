# 10 — Agents

## Fresher

**Concepts**: what an agent is (LLM + tools + loop), ReAct pattern (reason-act-observe), the basic agent loop from Topic 06's tool-calling demo, extended into multiple iterations.

**Resources**:
- [Anthropic — Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Prompting Guide — ReAct](https://www.promptingguide.ai/techniques/react)

**Code** (`code/01-fresher/`):
- `react_agent_basic.py` — single-tool agent loop (calculator or search-mock), runs until it produces a final answer, capped iteration count

**Interview questions**:
- What stops an agent from looping forever? (Max iteration cap, explicit termination conditions, or the model itself deciding it has enough info — all three should be in place in production.)

## Intermediate

**Concepts**: multi-tool agents, planning (decompose task into subtasks before acting), memory (short-term conversation buffer vs long-term retrieval-based memory), LangGraph basics (nodes, edges, state), simple multi-agent handoff (one agent delegates to another).

**Resources**:
- LangGraph — Quickstart (verify current API — this framework changes fast)
- Anthropic — Building Effective Agents, "workflows vs agents" section

**Code** (`code/02-intermediate/`):
- `langgraph_multi_tool_agent/` — agent with 3+ tools, explicit planning step before execution
- `agent_with_memory.py` — long-running conversation where agent retrieves relevant past interactions (reuses the Topic 07/08 RAG pipeline as memory backend)

**Interview questions**:
- What's the difference between a "workflow" and an "agent" in Anthropic's own framing? (Workflows: predefined code paths orchestrating LLM calls. Agents: the LLM dynamically decides its own path/tool sequence. Know when each is appropriate — workflows are more reliable/debuggable.)

## Advanced / Senior

**Concepts**: multi-agent orchestration (supervisor/worker patterns, parallel sub-agents), agent state management across long-running sessions, handling agent failures gracefully mid-task, cost-aware agent design (limiting expensive sub-agent spawns), evaluating agent trajectories (not just final answers — did it take a sane path?).

**Resources**:
- LangGraph — Multi-agent systems (verify current docs)
- [Anthropic — Multi-agent research system engineering post](https://www.anthropic.com/engineering/multi-agent-research-system)

**Code** (`code/03-advanced/`):
- `supervisor_worker_agents/` — supervisor agent decomposes a research task, spawns 2-3 worker sub-agents in parallel, aggregates results
- `agent_trajectory_eval.py` — log and score full agent trajectories (tool calls made, order, redundancy) not just final output

**Interview questions**:
- Your multi-agent system is 5x more expensive than a single-agent baseline for a marginal quality gain. How do you decide if it's worth it, and how do you cut cost without losing quality? (Direct cost/quality tradeoff reasoning — cache shared context, reduce sub-agent count, use cheaper models for sub-agents, reserve top-tier model for the supervisor/final synthesis.)

## Milestone project (end of Phase 3, part 1)

A multi-agent research assistant — supervisor + 2 worker agents, using tools + the Topic 08 RAG pipeline as one of the tools, with trajectory logging.
