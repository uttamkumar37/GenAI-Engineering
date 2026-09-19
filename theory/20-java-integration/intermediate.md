# 20 — Java Integration — Intermediate

**Concepts**: structured output binding in Spring AI (mapping LLM JSON responses to Java records/POJOs), function calling from Java, integrating a vector store (pgvector) via Spring AI's VectorStore abstraction, building a RAG endpoint in a Spring Boot service.

**Resources**:
- [Spring AI — Structured Output](https://docs.spring.io/spring-ai/reference/api/structured-output-converter.html)
- [Spring AI — Vector Databases](https://docs.spring.io/spring-ai/reference/api/vectordbs.html)

**Code** (`code/20-java-integration/02-intermediate/`):
- `spring-ai-rag-service/` — full Spring Boot RAG endpoint: pgvector-backed retrieval + structured output binding to a Java record, mirroring the Python Topic 08 pipeline

**Interview questions**:
- You have an existing Spring Boot microservice architecture. Would you add GenAI capability as a new Java service using Spring AI, or as a separate Python service the Java app calls? (Depends on team's Python maturity, latency needs, and whether GenAI is core or peripheral to that service — a nuanced answer that plays to a dual-stack strength.)
