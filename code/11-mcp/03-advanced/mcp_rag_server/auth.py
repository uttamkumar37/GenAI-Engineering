from __future__ import annotations

import os
from dataclasses import dataclass


class AuthError(Exception):
    pass


@dataclass(frozen=True)
class Principal:
    client_id: str
    scopes: frozenset[str]


# demo token->principal map; a real deployment would validate signed tokens (e.g. JWT/OAuth)
# against an identity provider, never a hardcoded dict — never put real secrets here
_VALID_TOKENS = {
    "demo-readonly-token": Principal("demo-client", frozenset({"rag:read"})),
    "demo-admin-token": Principal("admin-client", frozenset({"rag:read", "rag:admin"})),
}


def authenticate(token: str | None) -> Principal:
    expected_env_token = os.environ.get("MCP_RAG_TOKEN")
    if expected_env_token and token == expected_env_token:
        return Principal("env-configured-client", frozenset({"rag:read"}))

    if not token or token not in _VALID_TOKENS:
        raise AuthError("invalid or missing auth token")
    return _VALID_TOKENS[token]


def require_scope(principal: Principal, scope: str) -> None:
    if scope not in principal.scopes:
        raise AuthError(f"principal '{principal.client_id}' lacks required scope '{scope}'")
