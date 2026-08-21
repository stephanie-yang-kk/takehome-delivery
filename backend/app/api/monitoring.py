from fastapi import APIRouter, Depends, Query

from app.api.deps import get_current_user
from app.api.dto.monitoring import (
    CreateMonitoringServiceRequest,
    MonitoringServiceListResponse,
    MonitoringServiceResponse,
)
from app.errors import AppError
from app.service import auth as auth_service
from app.service import monitoring as monitoring_service
from app.service.auth import User

router = APIRouter(prefix="/api/v1/services", tags=["monitoring"])


def _to_response(target: monitoring_service.MonitoringTarget) -> MonitoringServiceResponse:
    return MonitoringServiceResponse(
        id=target.id,
        name=target.name,
        target=target.target,
        description=target.description,
    )


@router.get("", response_model=MonitoringServiceListResponse)
def list_monitoring_services(
    page: int = Query(1),
    page_size: int = Query(20),
    user: User = Depends(get_current_user),
) -> MonitoringServiceListResponse:
    if page < 1:
        raise AppError(422, "invalid_page", "page must be >= 1")
    if page_size < 1 or page_size > 100:
        raise AppError(422, "invalid_page_size", "page_size must be between 1 and 100")
    items, total = monitoring_service.list_targets(page, page_size)
    return MonitoringServiceListResponse(
        items=[_to_response(item) for item in items],
        page=page,
        page_size=page_size,
        total=total,
    )


@router.post("", response_model=MonitoringServiceResponse, status_code=201)
def create_monitoring_service(
    body: CreateMonitoringServiceRequest,
    user: User = Depends(get_current_user),
) -> MonitoringServiceResponse:
    auth_service.require_admin(user)
    target = monitoring_service.create_target(body.name, body.target, body.description, user.username)
    return _to_response(target)
