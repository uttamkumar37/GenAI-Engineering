# 12 — Agent Reliability

## Fresher

**Concepts**: why agents fail (tool errors, hallucinated tool args, infinite loops), basic retry logic, timeouts per tool call.

**Resources**:
- Anthropic — Building Effective Agents, "reliability" considerations section

**Code** (`code/01-fresher/`):
- `agent_with_retries.py` — wrap tool calls with retry + timeout, add to the Topic 10 basic agent

**Interview questions**:
- What's the difference between retrying a failed LLM call and retrying a failed tool call — should you handle them the same way? (LLM call failure = infra issue, safe to retry as-is; tool call failure might mean the model chose wrong args — retrying identically won't help, may need to re-prompt with the error.)

## Intermediate

**Concepts**: human-in-the-loop checkpoints (pause for approval before risky actions), state persistence (resuming an agent after a crash), structured error feedback to the model (so it can self-correct), cost tracking per agent run.

**Resources**:
- LangGraph — Human-in-the-loop (verify current API)

**Code** (`code/02-intermediate/`):
- `agent_human_approval.py` — agent pauses before any "write" action (e.g. sending an email-mock) and waits for approval
- `agent_state_checkpoint.py` — persist agent state to disk/DB, resume mid-task after simulated crash

**Interview questions**:
- Design a human-in-the-loop checkpoint for an agent that can modify a production database. What exactly gets shown to the human, and what's the failure mode if they don't respond? (Show the proposed action + reasoning + diff; timeout should default to safe/no-op, never default to proceeding.)

## Advanced / Senior

**Concepts**: cost control at scale (per-user/per-session budget caps, killing runaway agents), comprehensive state management for long-running multi-step agents (durable execution), observability into agent decision-making for debugging failures, designing graceful degradation (agent falls back to simpler behavior when a tool/sub-agent is unavailable).

**Resources**: 
- [Temporal — durable execution concepts](https://temporal.io/blog/what-is-durable-execution) (conceptual, even without adopting Temporal itself)

**Code** (`code/03-advanced/`):
- `agent_cost_budget_enforcer.py` — hard-stop an agent run when token/dollar budget is exceeded mid-task, with graceful partial-result return
- `agent_observability_wrapper.py` — full trace of every decision/tool call/cost, exportable for debugging (foundation for Topic 18 tracing)

**Interview questions**:
- An agent in production burned $400 overnight in a retry loop. Walk through the safeguards you'd put in place to prevent this from ever happening again. (Layered: per-call budget, per-session budget, max iteration cap, circuit breaker on repeated identical failures, alerting — not just one fix.)

## Milestone project (end of Phase 3)

Harden the Topic 10 multi-agent research assistant with human-in-the-loop approval, cost budgets, state persistence, and full trajectory observability — this is the Phase 3 capstone and a strong "I understand production AI, not just demos" story for interviews.
