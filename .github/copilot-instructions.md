# Repository Copilot Instructions

## Repository Overview

**GenAI-Engineering** is a topic-first learning repository taking a 6-year Java/Spring Boot engineer from fresher to advanced GenAI Engineer (LLM applications, agents, model customization). It has two parallel roots, `theory/` and `code/`, each covering the same 21 topics at three depths (fresher, intermediate, advanced/senior), plus milestone projects and interview notes.

## Technology Stack

Only what the repo declares:

- Python: consolidated `requirements.txt` (pydantic, FastAPI, uvicorn, pytest, hypothesis, httpx, numpy, pandas, matplotlib, torch, tiktoken, transformers, peft, trl, bitsandbytes, accelerate, datasets, anthropic, openai, ollama, boto3, langgraph, mcp, rank_bm25, sentence-transformers, networkx, psycopg/pgvector, qdrant-client, pymupdf/pypdf/pdfplumber/pytesseract, vllm, ragas, langfuse, structlog). It is a shared reference list, installed per topic as needed, not a pinned environment.
- Java: standalone Maven projects with their own `pom.xml` under `code/20-java-integration/` (Spring AI RAG service, Spring AI MCP client, Java-Python hybrid architecture)
- YAML: `code/19-deployment/03-advanced/ci_cd_pipeline.yml`
- No repo-level CI, Docker or Makefile.

## Repository Structure

```
theory/<NN-topic>/   README.md, fresher.md, intermediate.md, advanced.md   (concepts, resources, interview questions)
code/<NN-topic>/     01-fresher/ (one concept per script), 02-intermediate/ (realistic patterns), 03-advanced/ (production-grade, edge cases, tests)
milestones/          phase1..phase5-project, capstone-enterprise-assistant  (directories currently contain no files)
notes/               decision-framework, interview-questions, mock-interview-log, resume-bullets, system-design-scripts
requirements.txt, .gitignore
```

The 21 topics run from `01-python-for-ai` to `21-genai-system-design-interview-prep` (see README for the full ordered list).

## Architecture

Not an application. Each script or small package under `code/` is a self-contained demonstration of one concept. Intermediate/advanced pipelines are designed to run offline through fake/mock LLM clients; real provider calls are optional and clearly marked.

## Development Commands

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt          # or install only the packages a topic needs
python code/<topic>/01-fresher/<script>.py
pytest code/01-python-for-ai/02-intermediate/test_chat_api.py    # tests are per file/topic
# Java topics: cd into the specific project under code/20-java-integration/ and use its pom.xml (mvn)
```

Two Python test files exist today (`test_chat_api.py`, `test_provider_hypothesis.py` under `code/01-python-for-ai/`). Some topics need extra system tools or hardware: `tesseract` binary for OCR, a CUDA GPU for `vllm` (reference-only otherwise), local Ollama for `ollama_*` examples.

## Coding Guidelines

- Place new material in the matching `theory/<topic>/` and `code/<topic>/<tier>/` folders; keep the fresher -> intermediate -> advanced progression, and a topic's theory and code in step.
- Python: type hints, `pydantic` models for structured data, small functions, `async` only where the topic needs it; each script has a one-line header comment stating what it demonstrates and which API key (if any) it needs.
- Every script that needs a provider key must also have (or be paired with) a mock/fake client so it runs offline; default to the mock.
- Prefer the libraries already in `requirements.txt`; add new ones there only when a topic truly needs them.
- Fast-moving libraries (LangGraph, MCP SDK, peft/trl, ragas, langfuse, Spring AI, Bedrock) are listed in the README's "Known API-surface items to verify". Check the installed version before relying on an API, and keep version-sensitive caveats in comments.
- Java: standard Maven layout inside each project; do not merge them into one build.

## Testing

Add `pytest` tests for advanced-tier code (edge cases, property tests with `hypothesis` where useful) next to the code as `test_*.py`. Never present an LLM-dependent result as verified unless it was actually run; mock-based tests verify plumbing, not model quality. Say which was run.

## Security

- API keys (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, etc.) live only in a local `.env`, which is gitignored. Never commit keys, never print them, never hard-code them in examples.
- Guardrails/security topics (`17-guardrails-security`) demonstrate prompt-injection defenses; keep examples defensive and educational.
- `.gitignore` excludes `.env`, `.venv/`, model checkpoints (`*.safetensors`, `*.bin`, `checkpoints/`); do not add large model artifacts.

## Infrastructure / Deployment

No live infrastructure. Deployment material is illustrative: Bedrock adapter and a CI/CD pipeline YAML under `code/19-deployment/`. Treat the AWS Bedrock request shape as needing a check against current docs.

## Change Guidelines

1. Understand the existing implementation first.
2. Make the smallest coherent change.
3. Preserve the theory/code topic structure and numbering.
4. Do not introduce a new library when the existing stack already solves the requirement.
5. Update or add tests for behavior changes.
6. Run the touched script/tests before considering the change complete.
7. Do not leave commented-out code.
8. Do not leave TODO placeholders unless explicitly requested.
9. Do not fabricate implementation status.
10. Do not claim something was tested unless it was actually executed.

## Code Quality Rules

- Prefer readable code over clever code; avoid duplication and needless abstraction in teaching code.
- Follow existing naming (`snake_case` Python, numbered topic folders, tier folders `01-fresher`/`02-intermediate`/`03-advanced`).
- Handle edge cases and failures explicitly (timeouts, malformed model output, empty retrieval).
- Keep examples runnable as documented.
- Avoid unrelated refactoring during focused changes.

## Git Commit Rules

- Never add a `Co-Authored-By` trailer unless I explicitly request it.
- Never add Claude, Anthropic, GitHub Copilot, OpenAI, ChatGPT, Codex, Cursor, or any AI tool as an author or co-author.
- Use only the configured Git `user.name` and `user.email`.
- Do not mention AI assistance in commit messages.
- Keep commit messages concise and professional.
- Do not commit automatically unless I explicitly ask.
- Do not push automatically unless I explicitly ask.
- Never force-push unless I explicitly request it.
- Never rewrite Git history unless I explicitly request it.

## Git Commit Attribution Rules

- Never add a `Co-Authored-By` trailer for an AI system.
- Never add Claude, Anthropic, GitHub Copilot, OpenAI, ChatGPT, Codex, Cursor, Gemini, Devin, or any AI tool as an author or co-author.
- Never change Git author/committer identity to an AI account.
- Use only the configured human Git `user.name` and `user.email`.
- Do not add “Generated by AI”, “Created with AI”, or similar attribution to commit messages.
- Keep commit messages focused on the technical change.
- Do not commit automatically unless explicitly requested.
- Do not push automatically unless explicitly requested.
- Never rewrite Git history unless explicitly requested.

## AI Assistant Working Rules

When working in this repository:

- Inspect existing code before proposing architecture changes.
- Do not assume a feature exists without verifying it.
- Do not create fake implementations to make UI or tests appear complete.
- Do not generate random metrics, scores, or placeholder business data unless explicitly requested as test/demo data.
- Clearly separate verified behavior from assumptions.
- Prefer completing working vertical slices over creating many unfinished placeholders.
- Preserve repository conventions.
- Avoid massive rewrites unless explicitly requested.
- When fixing a bug, identify the underlying cause where practical.
- When adding functionality, consider error handling and tests.
- Never expose secrets, API keys, tokens, or credentials.
- Never hardcode secrets.

## Repository-Specific Rules (GenAI content)

- Keep depth honest at each tier: fresher = one concept per script; intermediate = combined realistic patterns; advanced = production-grade with edge cases and tests.
- Never fabricate evaluation numbers, benchmark results, model outputs or citations. Evaluation code (RAGAS-style, fallback scorers) must compute real values from real inputs; mock outputs must be labeled as mock.
- Comparisons of prompting vs RAG vs fine-tuning, and cost/latency claims, need a stated basis; do not present guesses as measurements.
- Milestone folders are currently empty; do not describe the milestone projects as built until code exists.
- Interview-prep notes (`notes/`) are the owner's; keep their framing and only add what is requested. Do not put unverified claims into `resume-bullets.md`.
