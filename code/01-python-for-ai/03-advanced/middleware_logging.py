from __future__ import annotations

import time
import uuid
from collections.abc import Awaitable, Callable

import structlog
from fastapi import FastAPI, Request, Response

logger = structlog.get_logger()


class CorrelationIdLoggingMiddleware:
    def __init__(self, app: FastAPI) -> None:
        self._app = app

    async def __call__(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        correlation_id = request.headers.get("x-correlation-id", str(uuid.uuid4()))
        start = time.monotonic()
        log = logger.bind(correlation_id=correlation_id, path=request.url.path, method=request.method)
        log.info("request_started")
        response = await call_next(request)
        duration_ms = (time.monotonic() - start) * 1000
        response.headers["x-correlation-id"] = correlation_id
        log.info("request_finished", status_code=response.status_code, duration_ms=round(duration_ms, 2))
        return response


def create_app() -> FastAPI:
    app = FastAPI(title="middleware-logging-demo")
    middleware = CorrelationIdLoggingMiddleware(app)
    app.middleware("http")(middleware.__call__)

    @app.get("/ping")
    async def ping() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
