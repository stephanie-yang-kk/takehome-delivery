from datetime import datetime, timezone

from app import config


def now() -> datetime:
    iso = config.test_clock_iso()
    if config.test_clock_enabled() and iso:
        return datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return datetime.now(timezone.utc)
