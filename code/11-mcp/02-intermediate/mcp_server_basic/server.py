from __future__ import annotations

# written against the `mcp` python sdk's FastMCP server pattern (mcp>=1.0); verify current
# API with `pip show mcp` since the SDK is young and evolving quickly
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("basic-tools-server")

# self-contained in-memory corpus standing in for the Topic 07 pgvector store (not yet
# implemented in this repo) so this server has no external dependency
DOCUMENTS = {
    "doc1": "MCP standardizes how LLM applications connect to external tools and data sources.",
    "doc2": "A vector database stores embeddings for fast approximate nearest-neighbor search.",
    "doc3": "LoRA fine-tuning trains small low-rank adapter matrices instead of full model weights.",
}


@mcp.tool()
def calculator(expression: str) -> str:
    allowed = set("0123456789.+-*/() ")
    if not set(expression) <= allowed:
        return "error: invalid characters in expression"
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as exc:
        return f"error: {exc}"


@mcp.tool()
def document_search(query: str) -> str:
    query_words = set(query.lower().split())
    scored = sorted(
        DOCUMENTS.items(),
        key=lambda item: len(query_words & set(item[1].lower().split())),
        reverse=True,
    )
    best_id, best_text = scored[0]
    if not (query_words & set(best_text.lower().split())):
        return "no matching document found"
    return f"{best_id}: {best_text}"


@mcp.resource("documents://list")
def list_documents() -> str:
    return "\n".join(f"{doc_id}: {text[:40]}..." for doc_id, text in DOCUMENTS.items())


if __name__ == "__main__":
    mcp.run(transport="stdio")
