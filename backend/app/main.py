import logging

from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.monitoring import router as monitoring_router
from app.api.observability import router as observability_router
from app.db.database import init_db
from app.errors import AppError, app_error_handler, unhandled_error_handler
from app.middleware.request_id import RequestIdMiddleware

logging.basicConfig(level=logging.INFO)


def create_app() -> FastAPI:
    app = FastAPI(title="Service Monitor")
    app.add_middleware(RequestIdMiddleware)
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(Exception, unhandled_error_handler)

    app.include_router(auth_router)
    app.include_router(monitoring_router)
    app.include_router(observability_router)

    @app.on_event("startup")
    def on_startup() -> None:
        init_db()

    return app


app = create_app()
