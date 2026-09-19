# 10 — Agents — Fresher

**Concepts**: what an agent is (LLM + tools + loop), ReAct pattern (reason-act-observe), the basic agent loop from Topic 06's tool-calling demo, extended into multiple iterations.

**Resources**:
- [Anthropic — Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Prompting Guide — ReAct](https://www.promptingguide.ai/techniques/react)

**Code** (`code/10-agents/01-fresher/`):
- `react_agent_basic.py` — single-tool agent loop (calculator or search-mock), runs until it produces a final answer, capped iteration count

**Interview questions**:
- What stops an agent from looping forever? (Max iteration cap, explicit termination conditions, or the model itself deciding it has enough info — all three should be in place in production.)
