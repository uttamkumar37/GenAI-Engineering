# 11 — MCP (Model Context Protocol) — Intermediate

**Concepts**: building a basic MCP server (exposing a tool, e.g. a file-search or database-query tool), building an MCP client that connects to it, resource exposure (read-only data the model can pull in).

**Resources**:
- [MCP docs — Build a server (Python SDK)](https://modelcontextprotocol.io/quickstart/server)
- [MCP docs — Build a client](https://modelcontextprotocol.io/quickstart/client)

**Code** (`code/11-mcp/02-intermediate/`):
- `mcp_server_basic/` — expose 2 tools (e.g. query the Topic 07 pgvector store, and a calculator) via MCP
- `mcp_client_basic/` — connect a client to it and drive a conversation using the exposed tools

**Interview questions**:
- Walk through what happens end-to-end when an MCP client calls a tool on your server. (Client discovers available tools/resources → sends tool-call request per protocol → server executes → returns structured result → client feeds back to the model.)
