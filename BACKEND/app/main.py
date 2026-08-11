from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import text

from app.api.router import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.session import engine


class HealthResponse(BaseModel):
    status: str


class DependencyStatus(BaseModel):
    status: str


class ReadinessResponse(BaseModel):
    status: str
    dependencies: dict[str, DependencyStatus]


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    yield


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(settings.frontend_origin)],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "Idempotency-Key"],
    )

    app.include_router(api_router, prefix=settings.api_v1_prefix)

    @app.get(
        "/health",
        response_model=HealthResponse,
        tags=["health"],
    )
    def health() -> HealthResponse:
        return HealthResponse(status="ok")

    @app.get(
        "/ready",
        response_model=ReadinessResponse,
        tags=["health"],
    )
    def ready() -> ReadinessResponse:
        if engine is None:
            return ReadinessResponse(
                status="ready",
                dependencies={
                    "database": DependencyStatus(status="not_configured")
                },
            )

        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail={
                    "status": "not_ready",
                    "dependencies": {
                        "database": {"status": "error"}
                    },
                },
            )

        return ReadinessResponse(
            status="ready",
            dependencies={
                "database": DependencyStatus(status="ok")
            },
        )

    return app


app = create_app()
