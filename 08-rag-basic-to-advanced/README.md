# 08 — RAG: Basic to Advanced

## Fresher

**Concepts**: the basic RAG loop (retrieve → augment prompt → generate), why RAG reduces hallucination, simple single-collection RAG.

**Resources**:
- [Pinecone — What is Retrieval-Augmented Generation](https://www.pinecone.io/learn/retrieval-augmented-generation/)

**Code** (`code/01-fresher/`):
- `basic_rag_pipeline.py` — embed a small doc set, retrieve top-3 on a query, stuff into prompt, generate answer

**Interview questions**:
- Why does RAG reduce but not eliminate hallucination? (Model can still misread or overgeneralize from retrieved context, or retrieval itself can miss the right chunk.)

## Intermediate

**Concepts**: query rewriting/expansion, multi-query retrieval, citation generation (tracing answer back to source chunks), conversational RAG (handling follow-up questions with context), evaluating retrieval quality manually.

**Resources**:
- LangChain — Query transformation strategies (verify current API)
- [Anthropic — Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)

**Code** (`code/02-intermediate/`):
- `query_rewriting_rag.py` — rewrite ambiguous follow-up questions using conversation history before retrieval
- `citation_tracking_rag.py` — return answer with inline citations mapping to source chunk IDs

**Interview questions**:
- A user asks a follow-up question that only makes sense given the previous turn. How does this break naive RAG, and how do you fix it? (Retrieval on the raw follow-up alone misses context — query rewriting using conversation history fixes it.)

## Advanced / Senior

**Concepts**: GraphRAG (entity/relationship extraction, graph-based retrieval for multi-hop questions), agentic RAG (model decides whether/what to retrieve, iterative retrieval), self-correction/verification loops (does retrieved context actually support the answer?), production RAG architecture (caching, incremental re-indexing, handling document updates/deletes).

**Resources**:
- [Microsoft Research — GraphRAG](https://microsoft.github.io/graphrag/)
- [Anthropic — Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) (verify link, this evolves)

**Code** (`code/03-advanced/`):
- `graphrag_minimal/` — extract entities/relations from a small doc set, build a graph, answer a multi-hop question that flat RAG fails on
- `agentic_rag_loop.py` — model iteratively decides to retrieve more, refine query, or answer
- `self_verification_rag.py` — after generation, run a second pass checking if the answer is actually supported by retrieved chunks, flag if not

**Interview questions**:
- When would you reach for GraphRAG instead of standard vector RAG? (Multi-hop reasoning across entities/relationships that a single similarity search can't surface — but be honest about its cost/complexity tradeoff.)

## Milestone project (end of Phase 2)

A full RAG application — hybrid search + reranking + query rewriting + citations + a simple eval script — over a real, moderately large document set (100+ pages), served via FastAPI with a minimal frontend or CLI. First strong portfolio piece.
