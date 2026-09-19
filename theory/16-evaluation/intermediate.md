# 16 — Evaluation — Intermediate

**Concepts**: LLM-as-judge (using a strong model to grade outputs against a rubric), RAGAS metrics (faithfulness, answer relevance, context precision/recall), building a growing eval dataset from real failures, regression testing basics (comparing scores across code changes).

**Resources**:
- [RAGAS docs — Getting Started](https://docs.ragas.io/en/stable/getstarted/)
- Anthropic — building evals guidance (verify current doc name)

**Code** (`code/16-evaluation/02-intermediate/`):
- `llm_as_judge.py` — grade the RAG pipeline's answers against a rubric using a second model call, with structured scoring output
- `ragas_eval_rag.py` — run RAGAS metrics on the Topic 08 RAG pipeline outputs

**Interview questions**:
- What are the failure modes of using an LLM to judge another LLM's output, and how do you mitigate them? (Judge bias toward verbose/confident-sounding answers, judge model's own blind spots, self-preference bias if same model family — mitigate with rubric specificity, multiple judge calls, calibration against human-labeled examples.)
