from fastapi import APIRouter, Depends, Query, Request

from app.api.deps import get_current_user
from app.api.dto.observability import MetricsResponse, StatusResponse
from app.errors import AppError
from app.service import monitoring as monitoring_service
from app.service import observability as observability_service
from app.service.auth import User

router = APIRouter(prefix="/api/v1/services", tags=["observability"])

SUPPORTED_WINDOWS = {"60s", "300s"}


def parse_window(raw: str | None) -> int:
    if raw is None:
        return 60
    if raw not in SUPPORTED_WINDOWS:
        raise AppError(422, "invalid_window", f"unsupported window: {raw}")
    return int(raw.removesuffix("s"))


@router.get("/{service_id}/status", response_model=StatusResponse)
async def get_service_status(
    service_id: str,
    request: Request,
    user: User = Depends(get_current_user),
) -> StatusResponse:
    target = monitoring_service.get_target(service_id)
    result = await observability_service.get_status(target.target, request.state.request_id)
    return StatusResponse(
        service_id=target.id,
        status=result.status,
        data_state=result.data_state,
        observed_at=result.observed_at.isoformat() if result.observed_at else None,
        age_seconds=result.age_seconds,
        request_id=request.state.request_id,
    )


@router.get("/{service_id}/metrics", response_model=MetricsResponse)
async def get_service_metrics(
    service_id: str,
    request: Request,
    window: str | None = Query(None),
) -> MetricsResponse:
    target = monitoring_service.get_target(service_id)
    window_seconds = parse_window(window)
    result = await observability_service.get_metrics(target.target, window_seconds, request.state.request_id)
    return MetricsResponse(
        service_id=target.id,
        as_of=result.as_of.isoformat(),
        window_seconds=result.window_seconds,
        known_seconds=result.known_seconds,
        unknown_seconds=result.unknown_seconds,
        durations_seconds=result.durations_seconds,
        data_state=result.data_state,
        request_id=request.state.request_id,
    )
