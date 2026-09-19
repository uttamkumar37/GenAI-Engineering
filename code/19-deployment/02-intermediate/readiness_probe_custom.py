from __future__ import annotations

import os

import httpx
import psycopg
from fastapi import FastAPI, Response

app = FastAPI()


def _check_llm_provider() -> bool:
    # lightweight reachability check — hits the provider's models endpoint, not a full completion
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return False
    try:
        resp = httpx.get(
            "https://api.openai.com/v1/models",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=3.0,
        )
        return resp.status_code == 200
    except httpx.HTTPError:
        return False


def _check_vector_db() -> bool:
    database_url = os.environ.get("DATABASE_URL", "")
    if not database_url:
        return False
    try:
        with psycopg.connect(database_url, connect_timeout=3) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
        return True
    except psycopg.Error:
        return False


@app.get("/healthz")
def liveness() -> dict[str, str]:
    # process-is-alive only, no downstream checks
    return {"status": "alive"}


@app.get("/readyz")
def readiness(response: Response) -> dict[str, object]:
    llm_ok = _check_llm_provider()
    db_ok = _check_vector_db()
    ready = llm_ok and db_ok
    response.status_code = 200 if ready else 503
    return {"ready": ready, "llm_provider": llm_ok, "vector_db": db_ok}
