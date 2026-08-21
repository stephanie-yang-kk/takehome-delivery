import sqlite3
from contextlib import contextmanager

from app import config

# Persists admin-created monitoring targets (GET/POST /api/v1/services).

SCHEMA = """
CREATE TABLE IF NOT EXISTS monitoring_services (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    target TEXT NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    occurred_at TEXT NOT NULL,
    action TEXT NOT NULL,
    actor TEXT NOT NULL,
    resource_id TEXT NOT NULL,
    detail TEXT
);
"""


def init_db() -> None:
    config.DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with connect() as conn:
        conn.executescript(SCHEMA)


@contextmanager
def connect():
    conn = sqlite3.connect(config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()
