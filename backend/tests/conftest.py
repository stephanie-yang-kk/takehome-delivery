import pytest
from fastapi.testclient import TestClient

from app import config
from app.db.database import init_db
from app.main import create_app
from app.db import cache


@pytest.fixture(autouse=True)
def reset_test_clock(monkeypatch):
    monkeypatch.delenv("TEST_CLOCK_ENABLED", raising=False)
    monkeypatch.delenv("TEST_CLOCK_ISO", raising=False)
    cache.clear()
    yield
    cache.clear()


@pytest.fixture
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(config, "DATABASE_PATH", db_path)
    init_db()
    app = create_app()
    with TestClient(app) as test_client:
        yield test_client


def login(client: TestClient, username: str, password: str) -> str:
    response = client.post("/api/v1/auth/login", json={"username": username, "password": password})
    assert response.status_code == 200
    return response.json()["token"]
