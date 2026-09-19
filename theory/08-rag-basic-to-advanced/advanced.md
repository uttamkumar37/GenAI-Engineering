# 08 — RAG: Basic to Advanced — Advanced / Senior

**Concepts**: GraphRAG (entity/relationship extraction, graph-based retrieval for multi-hop questions), agentic RAG (model decides whether/what to retrieve, iterative retrieval), self-correction/verification loops (does retrieved context actually support the answer?), production RAG architecture (caching, incremental re-indexing, handling document updates/deletes).

**Resources**:
- [Microsoft Research — GraphRAG](https://microsoft.github.io/graphrag/)
- [Anthropic — Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) (verify link, this evolves)

**Code** (`code/08-rag-basic-to-advanced/03-advanced/`):
- `graphrag_minimal/` — extract entities/relations from a small doc set, build a graph, answer a multi-hop question that flat RAG fails on
- `agentic_rag_loop.py` — model iteratively decides to retrieve more, refine query, or answer
- `self_verification_rag.py` — after generation, run a second pass checking if the answer is actually supported by retrieved chunks, flag if not

**Interview questions**:
- When would you reach for GraphRAG instead of standard vector RAG? (Multi-hop reasoning across entities/relationships that a single similarity search can't surface — but be honest about its cost/complexity tradeoff.)
