# 01 — Python for AI — Advanced / Senior

**Concepts**: structured concurrency (task groups, cancellation, `asyncio.TaskGroup` in 3.11+), backpressure and semaphores for rate-limited concurrent LLM calls, Pydantic v2 custom serializers/discriminated unions for polymorphic tool schemas, FastAPI middleware (request logging, retry-safe idempotency), dependency injection for swappable LLM providers (interface + multiple implementations — same pattern as a Spring `@Qualifier`), property-based testing (`hypothesis`) for validation logic, structured logging with `structlog`.

**Resources**:
- [Python docs — asyncio Task Groups](https://docs.python.org/3/library/asyncio-task.html#task-groups)
- [Pydantic v2 — Discriminated Unions](https://docs.pydantic.dev/latest/concepts/unions/#discriminated-unions)
- [FastAPI — Advanced Middleware](https://fastapi.tiangolo.com/advanced/middleware/)

**Code** (`code/01-python-for-ai/03-advanced/`):
- `llm_provider_abstraction/` — abstract `LLMProvider` interface, 3 concrete implementations (mocked Claude/OpenAI/Gemini clients), swappable via dependency injection, semaphore-limited concurrency (max N in-flight calls), per-provider circuit breaker (fail-fast after N consecutive errors)
- `structured_tool_schema.py` — discriminated union Pydantic model representing 3 different tool-call shapes (mirrors real function-calling payloads), with custom validators that produce LLM-readable error messages
- `test_provider_hypothesis.py` — hypothesis-based property tests on the validation logic
- `middleware_logging.py` — FastAPI middleware logging request/response with correlation IDs (foundation for tracing in Phase 5)

**Interview questions**:
- You have 3 LLM providers behind one interface, and one starts timing out intermittently. Design the resilience pattern. (Circuit breaker + timeout + fallback provider + structured logging to detect degradation — this is a system-design-style answer, not just code.)
- How would you rate-limit concurrent calls to an LLM API from an async FastAPI app without a queue system? (`asyncio.Semaphore`, explain why naive `gather` on 1000 items would violate provider rate limits.)
