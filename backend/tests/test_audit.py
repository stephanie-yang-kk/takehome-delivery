from app.db import audit as audit_db
from app.service.audit import ACTION_MONITORING_TARGET_CREATED
from tests.conftest import login


def test_create_service_writes_audit_log(client):
    token = login(client, "admin", "admin")
    response = client.post(
        "/api/v1/services",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Audited Target", "target": "svcD"},
    )
    assert response.status_code == 201
    service_id = response.json()["id"]

    logs = audit_db.list_for_resource(service_id)
    assert len(logs) == 1
    assert logs[0]["action"] == ACTION_MONITORING_TARGET_CREATED
    assert logs[0]["actor"] == "admin"
    assert logs[0]["resource_id"] == service_id
    assert "Audited Target" in logs[0]["detail"]
