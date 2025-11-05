"""Smoke tests for the FastAPI scaffold."""

from fastapi.testclient import TestClient

from app.main import app


def test_read_root() -> None:
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Hello from specDevAgent"}
