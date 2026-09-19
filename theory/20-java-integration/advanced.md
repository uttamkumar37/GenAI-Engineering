# 20 — Java Integration — Advanced / Senior

**Concepts**: production Spring AI service with observability (tying into Topic 18's tracing patterns from the Java side), calling Python-built MCP servers from a Java client (cross-language MCP interop), tool/function calling orchestration in Java for agent-like behavior, deciding architecture boundaries between Java (existing systems) and Python (AI/ML ecosystem) services in a real polyglot org.

**Resources**:
- [Spring AI — Tool Calling](https://docs.spring.io/spring-ai/reference/api/tools.html)
- MCP Java SDK, if available (verify at modelcontextprotocol.io — new territory)

**Code** (`code/20-java-integration/03-advanced/`):
- `spring-ai-mcp-client/` — Java client consuming the Topic 11 Python-built MCP server (cross-language interop is the differentiator here)
- `java-python-hybrid-architecture/` — a write-up + diagram of how to split a real GenAI product between Java (existing backend, auth, business logic) and Python (model-heavy pipelines), with the integration boundary explicitly designed

**Interview questions**:
- Design the architecture for adding a GenAI RAG feature into an existing large Java/Spring monolith without turning the whole thing into Python. Where's the boundary? (Signature interview answer — use MCP or a clean API boundary as the seam.)
