# 14 — Choosing Between Prompting, RAG, and Fine-Tuning — Advanced / Senior

Combining approaches (RAG + fine-tuning together, e.g. fine-tune for tool-use behavior + RAG for facts), knowing when NOT to build AI at all (a rules-based system may outperform an LLM for a narrow deterministic task).

**Resources**:
- [OpenAI — Fine-tuning guidance (compare against RAG)](https://platform.openai.com/docs/guides/fine-tuning)
- Your own before/after eval numbers from Topics 08 and 13 — use real data, not just theory

**Deliverable**: `notes/decision-framework.md` at repo root — a written framework recitable in an interview, backed by your own eval numbers comparing prompting-only vs RAG vs fine-tuned on the same task from your milestone projects.

**Interview questions**:
- A team wants to fine-tune a model because prompting "isn't accurate enough." What questions do you ask before agreeing? (Have they tried better prompting/few-shot first? Is the issue missing facts (RAG) vs wrong behavior (fine-tuning)? What's the cost of maintaining a fine-tuned model vs a RAG pipeline as data changes?)
