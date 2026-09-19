# GenAI Engineering — From Fresher to Advanced

Background: 6 years of software engineering (Java + Spring Boot). Target role: GenAI Engineer
(LLM applications, agents, model customization). This repo is organized **topic-first**, not
by calendar day, and split into two parallel root folders — `theory/` and `code/` — each
containing the same 21 topics, each topic covering fresher → intermediate → advanced/senior depth.

## Structure

```
theory/<topic>/
├── README.md        — overview, milestone, what to skip if behind
├── fresher.md        — concepts, resources, interview questions (fresher)
├── intermediate.md   — concepts, resources, interview questions (intermediate)
└── advanced.md       — concepts, resources, interview questions (advanced/senior)

code/<topic>/
├── 01-fresher/        — basic scripts, one concept each
├── 02-intermediate/   — combined, realistic patterns
└── 03-advanced/       — production-grade, edge cases, tests
```

Topics, in build order:

1. [Python for AI](theory/01-python-for-ai/README.md)
2. [Math & ML Essentials](theory/02-math-ml-essentials/README.md)
3. [Neural Networks & PyTorch](theory/03-neural-networks-pytorch/README.md)
4. [Transformers in Practice](theory/04-transformers-in-practice/README.md)
5. [LLM APIs](theory/05-llm-apis/README.md)
6. [Prompt Engineering](theory/06-prompt-engineering/README.md)
7. [Embeddings & Vector Databases](theory/07-embeddings-vector-db/README.md)
8. [RAG: Basic to Advanced](theory/08-rag-basic-to-advanced/README.md)
9. [Document Processing](theory/09-document-processing/README.md)
10. [Agents](theory/10-agents/README.md)
11. [MCP (Model Context Protocol)](theory/11-mcp/README.md)
12. [Agent Reliability](theory/12-agent-reliability/README.md)
13. [Fine-Tuning](theory/13-fine-tuning/README.md)
14. [Prompting vs RAG vs Fine-Tuning](theory/14-prompting-vs-rag-vs-finetune/README.md)
15. [Inference & Serving](theory/15-inference-serving/README.md)
16. [Evaluation](theory/16-evaluation/README.md)
17. [Guardrails & Security](theory/17-guardrails-security/README.md)
18. [LLMOps](theory/18-llmops/README.md)
19. [Deployment](theory/19-deployment/README.md)
20. [Java Integration](theory/20-java-integration/README.md)
21. [GenAI System Design & Interview Prep](theory/21-genai-system-design-interview-prep/README.md)

## Milestones

- `milestones/phase1-project/` — Transformers Internals Explainer
- `milestones/phase2-project/` — Hybrid-search + reranking + citations RAG app
- `milestones/phase3-project/` — Multi-agent research assistant with human-in-the-loop + cost control
- `milestones/phase4-project/` — QLoRA fine-tune with before/after eval
- `milestones/phase5-project/` — CI-gated eval pipeline + red-team report + LLMOps stack
- `milestones/capstone-enterprise-assistant/` — enterprise AI assistant: RAG + agents + MCP + evals + guardrails + cost/latency dashboard + Java/Spring AI client

## Notes

- `notes/interview-questions.md` — every interview question from every topic, answered in my own words
- `notes/resume-bullets.md` — resume bullets tied to real metrics from milestone projects
- `notes/system-design-scripts.md` — rehearsed GenAI system design answers
- `notes/mock-interview-log.md` — mock interview reflections

## Progress Log

One line per session, in the format: `- <date>: <what I built> — <what clicked>`
