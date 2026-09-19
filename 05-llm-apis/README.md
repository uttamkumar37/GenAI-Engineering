# 05 — LLM APIs

> Fast-moving section — verify model names, pricing, and API shapes against current provider docs before relying on anything here.

## Fresher

**Concepts**: making a basic API call to Claude/OpenAI/Gemini, API keys/env vars, request/response shape, streaming vs non-streaming basics.

**Resources**:
- [Anthropic — Messages API quickstart](https://docs.anthropic.com/en/api/getting-started)
- [OpenAI — Quickstart](https://platform.openai.com/docs/quickstart)

**Code** (`code/01-fresher/`):
- `basic_claude_call.py`, `basic_openai_call.py` — minimal scripts, `.env` for keys (never commit `.env` — already in `.gitignore`)

**Interview questions**:
- What's the difference between the Messages API and older completion-style APIs? (Structured turn-based roles vs raw text continuation.)

## Intermediate

**Concepts**: streaming responses (SSE handling), multi-turn conversation state management, system prompts vs user messages, provider-specific quirks (message role rules, max output tokens), local models via Ollama, running an open model via Hugging Face `transformers` pipeline.

**Resources**:
- [Anthropic — Streaming Messages](https://docs.anthropic.com/en/api/messages-streaming)
- [Ollama docs — Quickstart](https://ollama.com/docs)

**Code** (`code/02-intermediate/`):
- `streaming_chat_cli.py` — terminal chat loop with streaming output + conversation history
- `ollama_local_client.py` — same interface hitting a local Ollama model

**Interview questions**:
- How do you design a client abstraction that works identically for Claude, OpenAI, and a local Ollama model? (This is literally Topic 01's advanced provider-abstraction pattern — connect the dots explicitly.)

## Advanced / Senior

**Concepts**: unified multi-provider abstraction (reusing Topic 01's `LLMProvider` interface with real APIs), retry/backoff strategies per provider's rate-limit behavior, token counting and cost estimation pre-call, prompt caching (provider-specific, e.g. Anthropic prompt caching) for cost/latency reduction, handling provider outages with fallback chains.

**Resources**:
- [Anthropic — Prompt Caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [Anthropic — Rate Limits](https://docs.anthropic.com/en/api/rate-limits)

**Code** (`code/03-advanced/`):
- `unified_llm_gateway/` — provider abstraction (real APIs), automatic retry with exponential backoff, token/cost estimator, prompt-cache-aware request builder, fallback chain (Claude → OpenAI → local Ollama on failure)

**Interview questions**:
- Design a gateway that routes to the cheapest provider that meets a latency SLA, with automatic fallback on failure. (Real system-design interview question for GenAI roles — practice saying it out loud.)

## Milestone

The unified LLM gateway from Topics 01 + 05 becomes a reusable module imported into every project from here forward — don't rebuild provider logic per project.
