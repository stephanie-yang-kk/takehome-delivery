from app.clock import now
from app.db.database import connect


def insert(action: str, actor: str, resource_id: str, detail: str | None = None) -> None:
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO audit_logs (occurred_at, action, actor, resource_id, detail)
            VALUES (?, ?, ?, ?, ?)
            """,
            (now().isoformat(), action, actor, resource_id, detail),
        )


def list_for_resource(resource_id: str) -> list[dict[str, str | None]]:
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT action, actor, resource_id, detail
            FROM audit_logs
            WHERE resource_id = ?
            ORDER BY id
            """,
            (resource_id,),
        ).fetchall()
    return [dict(row) for row in rows]
