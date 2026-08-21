from dataclasses import dataclass
from datetime import datetime

from app.clock import now

STALE_SECONDS = 30


@dataclass
class CacheEntry:
    received_at: datetime
    payload: dict


_cache: dict[str, CacheEntry] = {}


def put(target: str, received_at: datetime, payload: dict) -> None:
    _cache[target] = CacheEntry(received_at=received_at, payload=payload)


def get_stale(target: str) -> CacheEntry | None:
    entry = _cache.get(target)
    if entry is None:
        return None
    age = (now() - entry.received_at).total_seconds()
    if age > STALE_SECONDS:
        return None
    return entry


def clear() -> None:
    _cache.clear()
