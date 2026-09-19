# 16 — Evaluation — Fresher

**Concepts**: why "it looks good to me" isn't evaluation, basic eval dataset structure (input, expected output/criteria), simple exact-match/rule-based scoring.

**Resources**:
- [Hamel Husain — Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/)

**Code** (`code/16-evaluation/01-fresher/`):
- `simple_eval_harness.py` — run 10 hand-written test cases against the Topic 08 RAG pipeline, rule-based pass/fail scoring

**Interview questions**:
- Why is manual spot-checking insufficient for evaluating an LLM feature before shipping? (Doesn't scale, isn't reproducible, misses regressions on edge cases, no historical comparison across versions.)
