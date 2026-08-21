from datetime import datetime, timezone

import pytest

from app.service.observability import compute_durations
from app.db import cache
from tests.conftest import login


@pytest.fixture(autouse=True)
def reset_cache():
    cache.clear()
    yield
    cache.clear()


def test_stale_cache_used_within_30_seconds(client, monkeypatch):
    admin_token = login(client, "admin", "admin")
    create = client.post(
        "/api/v1/services",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"name": "Stale Target", "target": "svcA"},
    )
    service_id = create.json()["id"]

    received_at = datetime(2026, 8, 21, 8, 0, 0, tzinfo=timezone.utc)
    cache.put(
        "svcA",
        received_at,
        {"name": "svcA", "current_status": "healthy", "history": []},
    )

    async def fail_fetch(target: str, request_id: str):
        return None, "unavailable"

    monkeypatch.setattr("app.service.observability.fetch_status", fail_fetch)
    monkeypatch.setenv("TEST_CLOCK_ENABLED", "true")
    monkeypatch.setenv("TEST_CLOCK_ISO", "2026-08-21T08:00:29+00:00")

    response = client.get(
        f"/api/v1/services/{service_id}/status",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    body = response.json()
    assert response.status_code == 200
    assert body["data_state"] == "stale"
    assert body["status"] == "healthy"


def test_stale_cache_rejected_after_30_seconds(client, monkeypatch):
    admin_token = login(client, "admin", "admin")
    create = client.post(
        "/api/v1/services",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"name": "Expired Target", "target": "svcB"},
    )
    service_id = create.json()["id"]

    received_at = datetime(2026, 8, 21, 8, 0, 0, tzinfo=timezone.utc)
    cache.put(
        "svcB",
        received_at,
        {"name": "svcB", "current_status": "healthy", "history": []},
    )

    async def fail_fetch(target: str, request_id: str):
        return None, "unavailable"

    monkeypatch.setattr("app.service.observability.fetch_status", fail_fetch)
    monkeypatch.setenv("TEST_CLOCK_ENABLED", "true")
    monkeypatch.setenv("TEST_CLOCK_ISO", "2026-08-21T08:00:31+00:00")

    response = client.get(
        f"/api/v1/services/{service_id}/status",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    body = response.json()
    assert response.status_code == 200
    assert body["data_state"] == "unavailable"
    assert body["status"] == "unknown"


def test_stale_limit_is_30_seconds_not_300():
    assert cache.STALE_SECONDS == 30


def test_metrics_initial_gap_counts_as_unknown():
    as_of = datetime(2026, 8, 21, 8, 1, 0, tzinfo=timezone.utc)
    history = [
        {"status": "healthy", "timestamp": "2026-08-21T08:00:40+00:00"},
    ]
    durations, unknown = compute_durations(history, 60, as_of)
    assert durations["healthy"] == 20.0
    assert unknown == 40.0
