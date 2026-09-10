"""Tests for the hosted playground HTTP endpoint."""

from __future__ import annotations

import pytest
from starlette.testclient import TestClient

from librarian_mcp.hosted import app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


@pytest.mark.parametrize("payload", [[], "text", 1])
def test_playground_rejects_non_object_json(client: TestClient, payload: object) -> None:
    response = client.post("/api/playground", json=payload)

    assert response.status_code == 400
    assert response.json() == {"error": "JSON body must be an object"}


def test_playground_rejects_json_null(client: TestClient) -> None:
    response = client.post(
        "/api/playground",
        content="null",
        headers={"content-type": "application/json"},
    )

    assert response.status_code == 400
    assert response.json() == {"error": "JSON body must be an object"}


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("intent", 123, "intent must be a string or a list of strings"),
        ("intent", ["canonical", 123], "intent must be a string or a list of strings"),
        ("max_tokens", "16000", "max_tokens must be a non-negative integer"),
        ("max_tokens", -1, "max_tokens must be a non-negative integer"),
        ("max_tokens", True, "max_tokens must be a non-negative integer"),
    ],
)
def test_playground_rejects_invalid_field_types(
    client: TestClient, field: str, value: object, message: str
) -> None:
    response = client.post("/api/playground", json={field: value})

    assert response.status_code == 400
    assert response.json() == {"error": message}


def test_playground_accepts_valid_request(client: TestClient) -> None:
    response = client.post("/api/playground", json={"intent": "", "max_tokens": 1})

    assert response.status_code == 200
    assert "packet" in response.json()
