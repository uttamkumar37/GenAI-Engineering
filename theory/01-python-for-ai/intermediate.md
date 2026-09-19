# 01 — Python for AI — Intermediate

**Concepts**: async/await + event loop, `asyncio.gather`/`asyncio.as_completed`, Pydantic v2 models + validators + `model_config`, FastAPI (path/query/body params, dependency injection, response models), pytest fixtures + parametrize, `uv` project management (pyproject.toml, lockfiles, dependency groups).

**Resources**:
- [Real Python — Async IO in Python: A Complete Walkthrough](https://realpython.com/async-io-python/)
- [Pydantic v2 docs — Validators](https://docs.pydantic.dev/latest/concepts/validators/)
- [FastAPI — full tutorial through Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [pytest docs — Fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)

**Code** (`code/01-python-for-ai/02-intermediate/`):
- `async_llm_client_mock.py` — async client class hitting 3 mocked "LLM providers" concurrently with `asyncio.gather`, timeout handling per call
- `chat_api/` — FastAPI app: `/chat` POST endpoint, Pydantic request/response models, a dependency-injected "settings" object (mirrors Spring's `@ConfigurationProperties`)
- `test_chat_api.py` — pytest with `TestClient`, fixtures for reusable test client, parametrized cases (valid, missing field, wrong type, empty string)

**Interview questions**:
- Your FastAPI endpoint calls an LLM API that takes 3-8 seconds. How do you keep the server responsive under load without async? (You mostly can't — sync blocks the worker; explain Uvicorn workers vs async event loop tradeoffs.)
- Why use Pydantic for LLM tool-call arguments instead of just parsing raw JSON? (Validation, coercion, clear error messages fed back to the model, schema generation for function-calling specs.)
