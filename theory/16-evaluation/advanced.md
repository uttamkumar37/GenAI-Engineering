# 16 — Evaluation — Advanced / Senior

**Concepts**: building a full eval suite that runs in CI on every PR (regression gating), eval dataset curation from production logs (finding real hard cases), multi-dimensional eval scoring (accuracy + latency + cost together), statistical significance when comparing prompt/model variants, human eval calibration against LLM-judge scores.

**Resources**:
- Search current Hamel Husain / Eugene Yan eval-driven development posts

**Code** (`code/16-evaluation/03-advanced/`):
- `eval_ci_pipeline/` — GitHub Actions workflow that runs the eval suite (RAGAS + LLM-judge + rule-based) on every push, fails the build if scores regress below a threshold
- `production_log_to_eval_case.py` — mines flagged/low-scoring production interactions into new eval test cases

**Interview questions**:
- Design an eval strategy for a RAG system used by 3 different teams for 3 different use cases. Should they share one eval suite? (No — shared infra/harness, but per-use-case eval datasets and thresholds, since "good" means different things per use case.)
