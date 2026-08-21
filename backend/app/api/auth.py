from fastapi import APIRouter

from app.api.dto.auth import LoginRequest, LoginResponse
from app.service import auth as auth_service

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def auth_login(body: LoginRequest) -> LoginResponse:
    token, role = auth_service.login(body.username, body.password)
    return LoginResponse(token=token, role=role)
