from dataclasses import dataclass
from uuid import uuid4

from app.errors import AppError

SEED_USERS = {
    "admin": {"password": "admin", "role": "admin"},
    "viewer": {"password": "viewer", "role": "viewer"},
}

_tokens: dict[str, dict[str, str]] = {}


@dataclass(frozen=True)
class User:
    username: str
    role: str


def login(username: str, password: str) -> tuple[str, str]:
    user = SEED_USERS.get(username)
    if user is None or user["password"] != password:
        raise AppError(401, "invalid_credentials", "Invalid username or password")
    token = str(uuid4())
    _tokens[token] = {"role": user["role"], "username": username}
    return token, user["role"]


def authenticate(token: str | None) -> User:
    if not token:
        raise AppError(401, "unauthorized", "Missing or invalid authentication")
    session = _tokens.get(token)
    if session is None:
        raise AppError(401, "unauthorized", "Missing or invalid authentication")
    return User(username=session["username"], role=session["role"])


def require_admin(user: User) -> None:
    if user.role != "admin":
        raise AppError(403, "forbidden", "Admin role required")
