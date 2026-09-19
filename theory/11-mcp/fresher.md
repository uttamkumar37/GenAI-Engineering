# 11 — MCP (Model Context Protocol) — Fresher

**Concepts**: what MCP is and why it exists (standardizing tool/context exposure to LLM clients instead of bespoke integrations per app), client vs server roles, resources vs tools vs prompts in the MCP spec.

**Resources**:
- [MCP official docs — Introduction](https://modelcontextprotocol.io/introduction)

**Code**: read + annotate the MCP spec's core concepts in this README; no code yet, just a working mental model.

**Interview questions**:
- How is MCP different from just defining tool-call schemas per provider? (Standard protocol any MCP-compatible client can consume, decoupling tool implementation from any single LLM provider's function-calling format.)
