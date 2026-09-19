from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from chat_api.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_chat_success(client: TestClient) -> None:
    response = client.post("/chat", json={"message": "hello", "user_id": "u1"})
    assert response.status_code == 200
    body = response.json()
    assert body["user_id"] == "u1"
    assert "hello" in body["reply"]


@pytest.mark.parametrize(
    ("payload", "expected_status"),
    [
        ({"message": "hi", "user_id": "u1"}, 200),
        ({"user_id": "u1"}, 422),
        ({"message": "hi", "user_id": "u1", "temperature": "hot"}, 422),
        ({"message": "", "user_id": "u1"}, 422),
    ],
)
def test_chat_validation(client: TestClient, payload: dict[str, object], expected_status: int) -> None:
    response = client.post("/chat", json=payload)
    assert response.status_code == expected_status
