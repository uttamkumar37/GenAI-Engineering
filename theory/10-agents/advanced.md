# 10 — Agents — Advanced / Senior

**Concepts**: multi-agent orchestration (supervisor/worker patterns, parallel sub-agents), agent state management across long-running sessions, handling agent failures gracefully mid-task, cost-aware agent design (limiting expensive sub-agent spawns), evaluating agent trajectories (not just final answers — did it take a sane path?).

**Resources**:
- LangGraph — Multi-agent systems (verify current docs)
- [Anthropic — Multi-agent research system engineering post](https://www.anthropic.com/engineering/multi-agent-research-system)

**Code** (`code/10-agents/03-advanced/`):
- `supervisor_worker_agents/` — supervisor agent decomposes a research task, spawns 2-3 worker sub-agents in parallel, aggregates results
- `agent_trajectory_eval.py` — log and score full agent trajectories (tool calls made, order, redundancy) not just final output

**Interview questions**:
- Your multi-agent system is 5x more expensive than a single-agent baseline for a marginal quality gain. How do you decide if it's worth it, and how do you cut cost without losing quality? (Direct cost/quality tradeoff reasoning — cache shared context, reduce sub-agent count, use cheaper models for sub-agents, reserve top-tier model for the supervisor/final synthesis.)
