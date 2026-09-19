# 21 — GenAI System Design, Resume, LinkedIn, Mock Interviews

Packaging topic — not a technical build. Everything else feeds into this.

## Fresher

Learn the standard GenAI system design interview format: clarify requirements → high-level architecture → deep-dive on 1-2 components → discuss tradeoffs/scale/cost.

**Resources**:
- [Hello Interview — ML/AI system design guides](https://www.hellointerview.com/) (check current AI-specific content)
- Your own capstone architecture as a worked example

## Intermediate

Write up 3-5 system design "scripts" adaptable live — e.g. "design a customer support RAG chatbot," "design a coding agent," "design a multi-tenant document Q&A system" — each grounded in decisions actually made in the capstone (chunking strategy, hybrid search, guardrails, eval gating, cost dashboard).

## Advanced / Senior

- **Resume**: translate each phase's milestone into a resume bullet with a measurable claim (e.g. "Built hybrid-search RAG pipeline with reranking, improving retrieval precision by X% per RAGAS eval" — use real eval numbers from Topic 16, never invented metrics).
- **LinkedIn**: publish the strongest milestone write-ups (RAG capstone, MCP server, QLoRA fine-tune, red-team report) as posts/articles — public artifacts are unusually persuasive for GenAI roles.
- **Mock interviews**: at least 3 full mock system-design interviews (record yourself, review), plus rapid-fire technical Q&A pulling from `notes/interview-questions.md` built up across all 20 prior topics.

**Deliverables**:
- `notes/resume-bullets.md`
- `notes/system-design-scripts.md`
- `notes/mock-interview-log.md`

**Interview questions (meta)**:
- Walk me through the hardest technical decision you made building your capstone, and what you'd do differently. (Asked in nearly every senior/mid GenAI interview — a well-reasoned tradeoff story beats a list of technologies used.)

## Job-readiness checklist (overall)

- [ ] Can explain attention/KV cache/sampling params without notes
- [ ] Can build a provider-agnostic LLM client from memory
- [ ] Has a working hybrid-search RAG app with citations, publicly on GitHub
- [ ] Has a working multi-agent system with guardrails and cost control
- [ ] Has built and deployed an MCP server
- [ ] Has one completed fine-tuning run with before/after eval numbers
- [ ] Has a CI pipeline that gates on eval scores
- [ ] Has a documented red-team exercise against their own system
- [ ] Can speak to Java/Python integration architecture specifically
- [ ] Has 3+ rehearsed system-design scripts and updated resume bullets tied to real metrics
