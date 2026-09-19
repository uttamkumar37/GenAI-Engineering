# 20 — Java Integration

This is the differentiator vs pure-Python/ML candidates — 6 years of Spring Boot experience applied directly to GenAI. Most GenAI Engineer candidates cannot speak to integrating GenAI into an existing enterprise Java system; this topic makes that a documented strength.

## Fresher

**Concepts**: Spring AI basics (ChatClient, basic prompt calls from Java), or LangChain4j basics — pick one to focus on, note the other exists.

**Resources**:
- [Spring AI — Reference docs, Getting Started](https://docs.spring.io/spring-ai/reference/getting-started.html) (verify current version — Spring AI is young and evolving fast)
- [LangChain4j — docs](https://docs.langchain4j.dev/)

**Code** (`code/01-fresher/`):
- `SpringAiBasicChat.java` — minimal Spring Boot app calling an LLM via Spring AI's ChatClient

**Interview questions**:
- As someone with 6 years of Spring Boot experience, what feels familiar vs genuinely new in Spring AI's abstractions? (DI patterns and starter/autoconfig style feel familiar; streaming and non-deterministic responses are the new part.)

## Intermediate

**Concepts**: structured output binding in Spring AI (mapping LLM JSON responses to Java records/POJOs), function calling from Java, integrating a vector store (pgvector) via Spring AI's VectorStore abstraction, building a RAG endpoint in a Spring Boot service.

**Resources**:
- [Spring AI — Structured Output](https://docs.spring.io/spring-ai/reference/api/structured-output-converter.html)
- [Spring AI — Vector Databases](https://docs.spring.io/spring-ai/reference/api/vectordbs.html)

**Code** (`code/02-intermediate/`):
- `spring-ai-rag-service/` — full Spring Boot RAG endpoint: pgvector-backed retrieval + structured output binding to a Java record, mirroring the Python Topic 08 pipeline

**Interview questions**:
- You have an existing Spring Boot microservice architecture. Would you add GenAI capability as a new Java service using Spring AI, or as a separate Python service the Java app calls? (Depends on team's Python maturity, latency needs, and whether GenAI is core or peripheral to that service — a nuanced answer that plays to a dual-stack strength.)

## Advanced / Senior

**Concepts**: production Spring AI service with observability (tying into Topic 18's tracing patterns from the Java side), calling Python-built MCP servers from a Java client (cross-language MCP interop), tool/function calling orchestration in Java for agent-like behavior, deciding architecture boundaries between Java (existing systems) and Python (AI/ML ecosystem) services in a real polyglot org.

**Resources**:
- [Spring AI — Tool Calling](https://docs.spring.io/spring-ai/reference/api/tools.html)
- MCP Java SDK, if available (verify at modelcontextprotocol.io — new territory)

**Code** (`code/03-advanced/`):
- `spring-ai-mcp-client/` — Java client consuming the Topic 11 Python-built MCP server (cross-language interop is the differentiator here)
- `java-python-hybrid-architecture/` — a write-up + diagram of how to split a real GenAI product between Java (existing backend, auth, business logic) and Python (model-heavy pipelines), with the integration boundary explicitly designed

**Interview questions**:
- Design the architecture for adding a GenAI RAG feature into an existing large Java/Spring monolith without turning the whole thing into Python. Where's the boundary? (Signature interview answer — use MCP or a clean API boundary as the seam.)

## Milestone

Make sure this topic's presentation explicitly frames it as the cross-stack differentiator for recruiters skimming the repo.
