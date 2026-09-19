# Splitting a GenAI Feature Between an Existing Java Monolith and Python Services

## Boundary decision

Keep the Java monolith owning auth, business rules, transactional data, and the public API surface.
Push model-heavy work (embeddings, RAG retrieval, agent orchestration, eval) into a separate Python
service. The seam between them is MCP (or a thin REST/gRPC API if MCP is overkill for the org) — not
a rewrite of the monolith and not a rewrite of the Python pipeline into Java.

## Diagram

```
                    ┌─────────────────────────────┐
                    │      Java Monolith           │
                    │  (Spring Boot)                │
                    │  - Auth / RBAC                │
                    │  - Business logic              │
                    │  - Transactional DB (existing) │
                    │  - Public REST API             │
                    └───────────────┬────────────────┘
                                    │ MCP client (tools/call)
                                    │  or REST/gRPC
                    ┌───────────────▼────────────────┐
                    │   Python GenAI Service          │
                    │  - RAG pipeline (Topic 08)       │
                    │  - MCP server (Topic 11)         │
                    │  - Embeddings + pgvector          │
                    │  - Eval gate (Topic 16)            │
                    └───────────────┬────────────────┘
                                    │
                    ┌───────────────▼────────────────┐
                    │  LLM providers / pgvector DB     │
                    └─────────────────────────────────┘
```

## Why here

- The monolith's auth and business rules are mature and expensive to port — leave them in Java.
- Python owns the ML ecosystem (embeddings, evals, agent frameworks) — re-implementing that in Java
  duplicates effort and lags the ecosystem.
- MCP gives a typed, introspectable tool boundary: the Java side calls `tools/list` + `tools/call`
  without knowing the Python implementation details, and the Python service can add new tools without
  a Java-side contract change.
- Alternative considered: full Spring AI in Java calling providers directly. Rejected here because the
  team's RAG/eval tooling (Topics 08/16) is already Python-native; duplicating it in Java doubles
  maintenance for no latency benefit (the extra network hop to the Python service is negligible next to
  LLM call latency).

## Tradeoffs to call out in an interview

- Extra hop (Java -> Python) adds latency; mitigate by keeping the boundary coarse (one RAG-answer call,
  not many small tool calls per request).
- Two deployable services means two on-call surfaces and two sets of observability tooling — worth it
  only once the GenAI surface area justifies a dedicated Python service (per Topic 19 discussion of
  self-hosted vs managed tradeoffs).
- If GenAI is peripheral (e.g., one summarization button), a same-process Spring AI call may be simpler
  than standing up a whole separate service — this pattern is for when GenAI is a growing product surface.
