# 12 — Agent Reliability — Intermediate

**Concepts**: human-in-the-loop checkpoints (pause for approval before risky actions), state persistence (resuming an agent after a crash), structured error feedback to the model (so it can self-correct), cost tracking per agent run.

**Resources**:
- LangGraph — Human-in-the-loop (verify current API)

**Code** (`code/12-agent-reliability/02-intermediate/`):
- `agent_human_approval.py` — agent pauses before any "write" action (e.g. sending an email-mock) and waits for approval
- `agent_state_checkpoint.py` — persist agent state to disk/DB, resume mid-task after simulated crash

**Interview questions**:
- Design a human-in-the-loop checkpoint for an agent that can modify a production database. What exactly gets shown to the human, and what's the failure mode if they don't respond? (Show the proposed action + reasoning + diff; timeout should default to safe/no-op, never default to proceeding.)
