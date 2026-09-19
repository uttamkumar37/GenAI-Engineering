# 11 — MCP (Model Context Protocol) — Advanced / Senior

**Concepts**: exposing the Phase 2 RAG pipeline as a full MCP server (tools + resources + prompts), authentication/authorization for MCP servers, connecting the MCP server to Claude Desktop or another real MCP client, multi-server orchestration (one client using several MCP servers together), error handling and reliability for MCP tool calls.

**Resources**:
- MCP docs — Security best practices (verify current spec section name)

**Code** (`code/11-mcp/03-advanced/`):
- `mcp_rag_server/` — production-style MCP server wrapping the RAG pipeline (search tool, document-list resource, citation-formatting prompt template), with auth and error handling; connect it to a real MCP client (e.g. Claude Desktop config) and demo it live

**Interview questions**:
- You're exposing an internal RAG system via MCP to multiple internal tools. What security concerns come up that didn't exist with a single bespoke integration? (Broader attack surface — any MCP client can now request data; need auth, scoping, rate limiting, and input validation on tool arguments.)
