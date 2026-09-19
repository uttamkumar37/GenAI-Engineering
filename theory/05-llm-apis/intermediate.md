# 05 — LLM APIs — Intermediate

**Concepts**: streaming responses (SSE handling), multi-turn conversation state management, system prompts vs user messages, provider-specific quirks (message role rules, max output tokens), local models via Ollama, running an open model via Hugging Face `transformers` pipeline.

**Resources**:
- [Anthropic — Streaming Messages](https://docs.anthropic.com/en/api/messages-streaming)
- [Ollama docs — Quickstart](https://ollama.com/docs)

**Code** (`code/05-llm-apis/02-intermediate/`):
- `streaming_chat_cli.py` — terminal chat loop with streaming output + conversation history
- `ollama_local_client.py` — same interface hitting a local Ollama model

**Interview questions**:
- How do you design a client abstraction that works identically for Claude, OpenAI, and a local Ollama model? (This is literally Topic 01's advanced provider-abstraction pattern — connect the dots explicitly.)
