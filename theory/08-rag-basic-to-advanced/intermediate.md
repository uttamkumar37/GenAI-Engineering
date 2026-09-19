# 08 — RAG: Basic to Advanced — Intermediate

**Concepts**: query rewriting/expansion, multi-query retrieval, citation generation (tracing answer back to source chunks), conversational RAG (handling follow-up questions with context), evaluating retrieval quality manually.

**Resources**:
- LangChain — Query transformation strategies (verify current API)
- [Anthropic — Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)

**Code** (`code/08-rag-basic-to-advanced/02-intermediate/`):
- `query_rewriting_rag.py` — rewrite ambiguous follow-up questions using conversation history before retrieval
- `citation_tracking_rag.py` — return answer with inline citations mapping to source chunk IDs

**Interview questions**:
- A user asks a follow-up question that only makes sense given the previous turn. How does this break naive RAG, and how do you fix it? (Retrieval on the raw follow-up alone misses context — query rewriting using conversation history fixes it.)
