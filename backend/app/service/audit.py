from app.db import audit as audit_db

ACTION_MONITORING_TARGET_CREATED = "monitoring_target.created"


def record_monitoring_target_created(
    actor: str,
    resource_id: str,
    name: str,
    upstream_target: str,
) -> None:
    detail = f"name={name}, upstream={upstream_target}"
    audit_db.insert(
        action=ACTION_MONITORING_TARGET_CREATED,
        actor=actor,
        resource_id=resource_id,
        detail=detail,
    )
