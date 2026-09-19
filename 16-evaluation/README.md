# 16 — Evaluation

## Fresher

**Concepts**: why "it looks good to me" isn't evaluation, basic eval dataset structure (input, expected output/criteria), simple exact-match/rule-based scoring.

**Resources**:
- [Hamel Husain — Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/)

**Code** (`code/01-fresher/`):
- `simple_eval_harness.py` — run 10 hand-written test cases against the Topic 08 RAG pipeline, rule-based pass/fail scoring

**Interview questions**:
- Why is manual spot-checking insufficient for evaluating an LLM feature before shipping? (Doesn't scale, isn't reproducible, misses regressions on edge cases, no historical comparison across versions.)

## Intermediate

**Concepts**: LLM-as-judge (using a strong model to grade outputs against a rubric), RAGAS metrics (faithfulness, answer relevance, context precision/recall), building a growing eval dataset from real failures, regression testing basics (comparing scores across code changes).

**Resources**:
- [RAGAS docs — Getting Started](https://docs.ragas.io/en/stable/getstarted/)
- Anthropic — building evals guidance (verify current doc name)

**Code** (`code/02-intermediate/`):
- `llm_as_judge.py` — grade the RAG pipeline's answers against a rubric using a second model call, with structured scoring output
- `ragas_eval_rag.py` — run RAGAS metrics on the Topic 08 RAG pipeline outputs

**Interview questions**:
- What are the failure modes of using an LLM to judge another LLM's output, and how do you mitigate them? (Judge bias toward verbose/confident-sounding answers, judge model's own blind spots, self-preference bias if same model family — mitigate with rubric specificity, multiple judge calls, calibration against human-labeled examples.)

## Advanced / Senior

**Concepts**: building a full eval suite that runs in CI on every PR (regression gating), eval dataset curation from production logs (finding real hard cases), multi-dimensional eval scoring (accuracy + latency + cost together), statistical significance when comparing prompt/model variants, human eval calibration against LLM-judge scores.

**Resources**:
- Search current Hamel Husain / Eugene Yan eval-driven development posts

**Code** (`code/03-advanced/`):
- `eval_ci_pipeline/` — GitHub Actions workflow that runs the eval suite (RAGAS + LLM-judge + rule-based) on every push, fails the build if scores regress below a threshold
- `production_log_to_eval_case.py` — mines flagged/low-scoring production interactions into new eval test cases

**Interview questions**:
- Design an eval strategy for a RAG system used by 3 different teams for 3 different use cases. Should they share one eval suite? (No — shared infra/harness, but per-use-case eval datasets and thresholds, since "good" means different things per use case.)

## Milestone project (Phase 5, part 1)

A CI-integrated eval pipeline running against the capstone RAG+agent system, with a dashboard of scores over time — separates "built a demo" from "built something production-credible."
