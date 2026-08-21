from dataclasses import dataclass
from datetime import datetime, timedelta

from app.clock import now
from app.db.cache import get_stale, put
from app.upstream.client import VALID_STATUSES, fetch_status


@dataclass
class StatusResult:
    status: str
    data_state: str
    observed_at: datetime | None
    age_seconds: float | None


@dataclass
class MetricsResult:
    as_of: datetime
    window_seconds: int
    known_seconds: float
    unknown_seconds: float
    durations_seconds: dict[str, float]
    data_state: str


def _normalize_status(raw: str | None) -> str:
    if raw in VALID_STATUSES:
        return raw
    return "unknown"


def _age_seconds(observed_at: datetime | None) -> float | None:
    if observed_at is None:
        return None
    return max(0.0, (now() - observed_at).total_seconds())


async def get_status(target: str, request_id: str) -> StatusResult:
    payload, _error = await fetch_status(target, request_id)
    received_at = now()
    if payload is not None:
        put(target, received_at, payload)
        return StatusResult(
            status=_normalize_status(payload.get("current_status")),
            data_state="fresh",
            observed_at=received_at,
            age_seconds=0.0,
        )

    cached = get_stale(target)
    if cached is not None:
        return StatusResult(
            status=_normalize_status(cached.payload.get("current_status")),
            data_state="stale",
            observed_at=cached.received_at,
            age_seconds=_age_seconds(cached.received_at),
        )

    return StatusResult(
        status="unknown",
        data_state="unavailable",
        observed_at=None,
        age_seconds=None,
    )


async def get_metrics(target: str, window_seconds: int, request_id: str) -> MetricsResult:
    as_of = now()
    payload, _error = await fetch_status(target, request_id)
    received_at = now()
    if payload is not None:
        put(target, received_at, payload)
        durations, unknown = compute_durations(payload.get("history", []), window_seconds, as_of)
        return MetricsResult(
            as_of=as_of,
            window_seconds=window_seconds,
            known_seconds=sum(durations.values()),
            unknown_seconds=unknown,
            durations_seconds=durations,
            data_state="fresh",
        )

    cached = get_stale(target)
    if cached is not None:
        durations, unknown = compute_durations(cached.payload.get("history", []), window_seconds, as_of)
        return MetricsResult(
            as_of=as_of,
            window_seconds=window_seconds,
            known_seconds=sum(durations.values()),
            unknown_seconds=unknown,
            durations_seconds=durations,
            data_state="stale",
        )

    return MetricsResult(
        as_of=as_of,
        window_seconds=window_seconds,
        known_seconds=0.0,
        unknown_seconds=float(window_seconds),
        durations_seconds={"healthy": 0.0, "degraded": 0.0, "down": 0.0},
        data_state="unavailable",
    )


def compute_durations(history: list, window_seconds: int, as_of: datetime) -> tuple[dict[str, float], float]:
    window_start = as_of - timedelta(seconds=window_seconds)
    durations = {"healthy": 0.0, "degraded": 0.0, "down": 0.0}

    events: list[tuple[datetime, str]] = []
    for item in history:
        if not isinstance(item, dict):
            continue
        status = item.get("status")
        timestamp = item.get("timestamp")
        if status not in VALID_STATUSES or not isinstance(timestamp, str):
            continue
        try:
            events.append((datetime.fromisoformat(timestamp.replace("Z", "+00:00")), status))
        except ValueError:
            continue

    events.sort(key=lambda item: item[0])
    if not events:
        return durations, float(window_seconds)

    prior = [event for event in events if event[0] <= window_start]
    in_window = [event for event in events if window_start < event[0] <= as_of]

    cursor = window_start
    current_status: str | None = prior[-1][1] if prior else None

    for event_time, status in in_window:
        if current_status is not None and event_time > cursor:
            durations[current_status] += (event_time - cursor).total_seconds()
        cursor = event_time
        current_status = status

    if current_status is not None and as_of > cursor:
        durations[current_status] += (as_of - cursor).total_seconds()

    known = sum(durations.values())
    unknown = max(0.0, float(window_seconds) - known)
    return durations, unknown
