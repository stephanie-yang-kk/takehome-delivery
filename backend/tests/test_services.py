from tests.conftest import login


def test_admin_can_create_service(client):
    token = login(client, "admin", "admin")
    response = client.post(
        "/api/v1/services",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Service A", "target": "svcA", "description": "primary"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Service A"
    assert body["target"] == "svcA"


def test_viewer_cannot_create_service(client):
    token = login(client, "viewer", "viewer")
    response = client.post(
        "/api/v1/services",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Blocked", "target": "svcB"},
    )
    assert response.status_code == 403
    assert response.json()["code"] == "forbidden"


def test_metrics_honors_requested_window(client):
    admin_token = login(client, "admin", "admin")
    create = client.post(
        "/api/v1/services",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"name": "Metrics Target", "target": "svcC"},
    )
    service_id = create.json()["id"]

    response = client.get(
        f"/api/v1/services/{service_id}/metrics?window=300s",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    assert response.json()["window_seconds"] == 300
