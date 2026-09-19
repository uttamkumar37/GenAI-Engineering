# 01 — Python for AI

## Fresher

**Concepts**: variables/types recap, functions, list/dict comprehensions, `*args`/`**kwargs`, virtual environments, type hints basics (`str`, `int`, `list[str]`, `Optional`).

**Resources**:
- [Python typing docs — typing module basics](https://docs.python.org/3/library/typing.html) (skim intro + common types)
- [Real Python — Python Type Checking Guide](https://realpython.com/python-type-checking/) (intro section only)

**Code** (`code/01-fresher/`):
- `type_hints_basics.py` — functions with full type annotations, run through `mypy`
- `list_dict_comprehensions.py` — data transformation drills (flatten, filter, group)
- `venv_setup.md` — notes on `uv init`, `uv add`, `uv run`

**Interview questions**:
- What's the difference between `list` and `List[str]` in type hints, and does Python enforce them at runtime? (No — hints are documentation + static-analysis only, unless you validate explicitly, which is exactly why Pydantic exists.)

## Intermediate

**Concepts**: async/await + event loop, `asyncio.gather`/`asyncio.as_completed`, Pydantic v2 models + validators + `model_config`, FastAPI (path/query/body params, dependency injection, response models), pytest fixtures + parametrize, `uv` project management (pyproject.toml, lockfiles, dependency groups).

**Resources**:
- [Real Python — Async IO in Python: A Complete Walkthrough](https://realpython.com/async-io-python/)
- [Pydantic v2 docs — Validators](https://docs.pydantic.dev/latest/concepts/validators/)
- [FastAPI — full tutorial through Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [pytest docs — Fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)

**Code** (`code/02-intermediate/`):
- `async_llm_client_mock.py` — async client class hitting 3 mocked "LLM providers" concurrently with `asyncio.gather`, timeout handling per call
- `chat_api/` — FastAPI app: `/chat` POST endpoint, Pydantic request/response models, a dependency-injected "settings" object (mirrors Spring's `@ConfigurationProperties`)
- `test_chat_api.py` — pytest with `TestClient`, fixtures for reusable test client, parametrized cases (valid, missing field, wrong type, empty string)

**Interview questions**:
- Your FastAPI endpoint calls an LLM API that takes 3-8 seconds. How do you keep the server responsive under load without async? (You mostly can't — sync blocks the worker; explain Uvicorn workers vs async event loop tradeoffs.)
- Why use Pydantic for LLM tool-call arguments instead of just parsing raw JSON? (Validation, coercion, clear error messages fed back to the model, schema generation for function-calling specs.)

## Advanced / Senior

**Concepts**: structured concurrency (task groups, cancellation, `asyncio.TaskGroup` in 3.11+), backpressure and semaphores for rate-limited concurrent LLM calls, Pydantic v2 custom serializers/discriminated unions for polymorphic tool schemas, FastAPI middleware (request logging, retry-safe idempotency), dependency injection for swappable LLM providers (interface + multiple implementations — same pattern as a Spring `@Qualifier`), property-based testing (`hypothesis`) for validation logic, structured logging with `structlog`.

**Resources**:
- [Python docs — asyncio Task Groups](https://docs.python.org/3/library/asyncio-task.html#task-groups)
- [Pydantic v2 — Discriminated Unions](https://docs.pydantic.dev/latest/concepts/unions/#discriminated-unions)
- [FastAPI — Advanced Middleware](https://fastapi.tiangolo.com/advanced/middleware/)

**Code** (`code/03-advanced/`):
- `llm_provider_abstraction/` — abstract `LLMProvider` interface, 3 concrete implementations (mocked Claude/OpenAI/Gemini clients), swappable via dependency injection, semaphore-limited concurrency (max N in-flight calls), per-provider circuit breaker (fail-fast after N consecutive errors)
- `structured_tool_schema.py` — discriminated union Pydantic model representing 3 different tool-call shapes (mirrors real function-calling payloads), with custom validators that produce LLM-readable error messages
- `test_provider_hypothesis.py` — hypothesis-based property tests on the validation logic
- `middleware_logging.py` — FastAPI middleware logging request/response with correlation IDs (foundation for tracing in Phase 5)

**Interview questions**:
- You have 3 LLM providers behind one interface, and one starts timing out intermittently. Design the resilience pattern. (Circuit breaker + timeout + fallback provider + structured logging to detect degradation — this is a system-design-style answer, not just code.)
- How would you rate-limit concurrent calls to an LLM API from an async FastAPI app without a queue system? (`asyncio.Semaphore`, explain why naive `gather` on 1000 items would violate provider rate limits.)

## Milestone checkpoint

Build a FastAPI service that calls multiple mocked LLM providers concurrently, validates all inputs/outputs with Pydantic, handles provider failures gracefully, and is fully covered by pytest — this exact shape reappears in Phase 2 with real APIs.

## If short on time

Fresher level can be skipped entirely if already comfortable with type hints and venvs — go straight to intermediate. Do not skip the advanced circuit-breaker/semaphore pattern — it resurfaces directly in Topic 12 (agent reliability) and Topic 18 (LLMOps fallbacks).
