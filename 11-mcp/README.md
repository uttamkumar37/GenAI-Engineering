# 11 — MCP (Model Context Protocol)

> Actively evolving spec — verify the current MCP spec version before building against it.

## Fresher

**Concepts**: what MCP is and why it exists (standardizing tool/context exposure to LLM clients instead of bespoke integrations per app), client vs server roles, resources vs tools vs prompts in the MCP spec.

**Resources**:
- [MCP official docs — Introduction](https://modelcontextprotocol.io/introduction)

**Code**: read + annotate the MCP spec's core concepts in this README; no code yet, just a working mental model.

**Interview questions**:
- How is MCP different from just defining tool-call schemas per provider? (Standard protocol any MCP-compatible client can consume, decoupling tool implementation from any single LLM provider's function-calling format.)

## Intermediate

**Concepts**: building a basic MCP server (exposing a tool, e.g. a file-search or database-query tool), building an MCP client that connects to it, resource exposure (read-only data the model can pull in).

**Resources**:
- [MCP docs — Build a server (Python SDK)](https://modelcontextprotocol.io/quickstart/server)
- [MCP docs — Build a client](https://modelcontextprotocol.io/quickstart/client)

**Code** (`code/02-intermediate/`):
- `mcp_server_basic/` — expose 2 tools (e.g. query the Topic 07 pgvector store, and a calculator) via MCP
- `mcp_client_basic/` — connect a client to it and drive a conversation using the exposed tools

**Interview questions**:
- Walk through what happens end-to-end when an MCP client calls a tool on your server. (Client discovers available tools/resources → sends tool-call request per protocol → server executes → returns structured result → client feeds back to the model.)

## Advanced / Senior

**Concepts**: exposing the Phase 2 RAG pipeline as a full MCP server (tools + resources + prompts), authentication/authorization for MCP servers, connecting the MCP server to Claude Desktop or another real MCP client, multi-server orchestration (one client using several MCP servers together), error handling and reliability for MCP tool calls.

**Resources**:
- MCP docs — Security best practices (verify current spec section name)

**Code** (`code/03-advanced/`):
- `mcp_rag_server/` — production-style MCP server wrapping the RAG pipeline (search tool, document-list resource, citation-formatting prompt template), with auth and error handling; connect it to a real MCP client (e.g. Claude Desktop config) and demo it live

**Interview questions**:
- You're exposing an internal RAG system via MCP to multiple internal tools. What security concerns come up that didn't exist with a single bespoke integration? (Broader attack surface — any MCP client can now request data; need auth, scoping, rate limiting, and input validation on tool arguments.)

## Milestone

The RAG system, now accessible as an MCP server, usable from Claude Desktop or any MCP-compatible client — a genuinely differentiating portfolio piece since most candidates haven't touched MCP hands-on yet.
