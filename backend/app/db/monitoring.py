from app.db.database import connect
from app.db.models import MonitoringRow


def count_all() -> int:
    with connect() as conn:
        return conn.execute("SELECT COUNT(*) FROM monitoring_services").fetchone()[0]


def list_all_monitors(page: int, page_size: int) -> list[MonitoringRow]:
    offset = (page - 1) * page_size
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT id, name, target, description
            FROM monitoring_services
            ORDER BY name
            LIMIT ? OFFSET ?
            """,
            (page_size, offset),
        ).fetchall()
    return [_to_po(row) for row in rows]


def get_monitor_by_service_id(service_id: str) -> MonitoringRow | None:
    with connect() as conn:
        row = conn.execute(
            "SELECT id, name, target, description FROM monitoring_services WHERE id = ?",
            (service_id,),
        ).fetchone()
    if row is None:
        return None
    return _to_po(row)


def insert_monitor(service_id: str, name: str, target: str, description: str | None) -> MonitoringRow:
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO monitoring_services (id, name, target, description)
            VALUES (?, ?, ?, ?)
            """,
            (service_id, name, target, description),
        )
    return MonitoringRow(id=service_id, name=name, target=target, description=description)


def _to_po(row) -> MonitoringRow:
    return MonitoringRow(
        id=row["id"],
        name=row["name"],
        target=row["target"],
        description=row["description"],
    )
