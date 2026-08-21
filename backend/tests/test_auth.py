from tests.conftest import login


def test_login_returns_token_and_role(client):
    response = client.post("/api/v1/auth/login", json={"username": "admin", "password": "admin"})
    assert response.status_code == 200
    body = response.json()
    assert body["role"] == "admin"
    assert body["token"]


def test_protected_route_requires_auth(client):
    response = client.get("/api/v1/services")
    assert response.status_code == 401
    assert response.json()["code"] == "unauthorized"
