# 12 — Agent Reliability — Advanced / Senior

**Concepts**: cost control at scale (per-user/per-session budget caps, killing runaway agents), comprehensive state management for long-running multi-step agents (durable execution), observability into agent decision-making for debugging failures, designing graceful degradation (agent falls back to simpler behavior when a tool/sub-agent is unavailable).

**Resources**: 
- [Temporal — durable execution concepts](https://temporal.io/blog/what-is-durable-execution) (conceptual, even without adopting Temporal itself)

**Code** (`code/12-agent-reliability/03-advanced/`):
- `agent_cost_budget_enforcer.py` — hard-stop an agent run when token/dollar budget is exceeded mid-task, with graceful partial-result return
- `agent_observability_wrapper.py` — full trace of every decision/tool call/cost, exportable for debugging (foundation for Topic 18 tracing)

**Interview questions**:
- An agent in production burned $400 overnight in a retry loop. Walk through the safeguards you'd put in place to prevent this from ever happening again. (Layered: per-call budget, per-session budget, max iteration cap, circuit breaker on repeated identical failures, alerting — not just one fix.)
