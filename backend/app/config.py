import os
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "data" / "app.db"
STATUS_SERVICE_URL = os.getenv("STATUS_SERVICE_URL", "http://localhost:8090").rstrip("/")


def test_clock_enabled() -> bool:
    return os.getenv("TEST_CLOCK_ENABLED", "").lower() in ("1", "true", "yes")


def test_clock_iso() -> str | None:
    return os.getenv("TEST_CLOCK_ISO")
