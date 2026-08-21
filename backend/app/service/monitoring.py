from dataclasses import dataclass
from uuid import uuid4

from app.db import monitoring as monitoring_db
from app.db.models import MonitoringRow
from app.errors import AppError
from app.service import audit as audit_service

VALID_TARGETS = {"svcA", "svcB", "svcC", "svcD", "svcE"}


@dataclass(frozen=True)
class MonitoringTarget:
    id: str
    name: str
    target: str
    description: str | None = None


def list_targets(page: int, page_size: int) -> tuple[list[MonitoringTarget], int]:
    total = monitoring_db.count_all()
    rows = monitoring_db.list_all_monitors(page, page_size)
    return [_to_bo(row) for row in rows], total


def get_target(service_id: str) -> MonitoringTarget:
    row = monitoring_db.get_monitor_by_service_id(service_id)
    if row is None:
        raise AppError(404, "not_found", "Monitoring target not found")
    return _to_bo(row)


def create_target(name: str, target: str, description: str | None, actor: str) -> MonitoringTarget:
    if target not in VALID_TARGETS:
        raise AppError(422, "invalid_target", f"target must be one of {sorted(VALID_TARGETS)}")
    row = monitoring_db.insert_monitor(str(uuid4()), name, target, description)
    created = _to_bo(row)
    audit_service.record_monitoring_target_created(actor, created.id, created.name, created.target)
    return created


def _to_bo(row: MonitoringRow) -> MonitoringTarget:
    return MonitoringTarget(
        id=row.id,
        name=row.name,
        target=row.target,
        description=row.description,
    )
