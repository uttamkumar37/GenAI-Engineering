from __future__ import annotations

# written against the `mcp` python sdk's FastMCP pattern (mcp>=1.0); the exact context-passing
# mechanism for per-call auth metadata has changed across SDK versions — verify current API
import logging
import os
import time
from collections import defaultdict

from mcp.server.fastmcp import FastMCP

from auth import AuthError, authenticate, require_scope
from rag_pipeline import retrieve

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_rag_server")

mcp = FastMCP("rag-server")

RATE_LIMIT_WINDOW_SECONDS = 60
RATE_LIMIT_MAX_CALLS = 30
_call_timestamps: dict[str, list[float]] = defaultdict(list)


def _check_rate_limit(client_id: str) -> None:
    now = time.time()
    window_start = now - RATE_LIMIT_WINDOW_SECONDS
    calls = [t for t in _call_timestamps[client_id] if t >= window_start]
    if len(calls) >= RATE_LIMIT_MAX_CALLS:
        raise AuthError(f"rate limit exceeded for client '{client_id}'")
    calls.append(now)
    _call_timestamps[client_id] = calls


def _authorize_request(token: str | None, scope: str):
    try:
        principal = authenticate(token)
        require_scope(principal, scope)
        _check_rate_limit(principal.client_id)
        return principal
    except AuthError as exc:
        logger.warning("auth rejected: %s", exc)
        raise


@mcp.tool()
def rag_search(query: str, auth_token: str) -> str:
    try:
        _authorize_request(auth_token, "rag:read")
    except AuthError as exc:
        return f"error: {exc}"

    if not query or not query.strip():
        return "error: query must not be empty"

    try:
        chunks = retrieve(query)
    except Exception as exc:
        logger.exception("retrieval failed")
        return f"error: retrieval failed ({exc})"

    if not chunks:
        return "no relevant documents found"

    return "\n".join(f"[{c.doc_id}] ({c.source}) {c.text}" for c in chunks)


@mcp.resource("documents://list")
def document_list() -> str:
    from rag_pipeline import CORPUS

    return "\n".join(f"{c.doc_id} ({c.source})" for c in CORPUS)


@mcp.prompt()
def citation_prompt(question: str, retrieved_text: str) -> str:
    return (
        f"Answer the question using only the sources below. Cite each fact as [doc_id].\n\n"
        f"Question: {question}\n\nSources:\n{retrieved_text}\n\nAnswer:"
    )


if __name__ == "__main__":
    if not os.environ.get("MCP_RAG_TOKEN"):
        logger.info("MCP_RAG_TOKEN not set; falling back to the demo token table in auth.py")
    mcp.run(transport="stdio")
