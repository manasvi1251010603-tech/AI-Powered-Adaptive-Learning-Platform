from __future__ import annotations

import logging
from uuid import uuid4

from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


def build_error_response(
    *,
    code: str,
    message: str,
    status_code: int,
    request_id: str,
    details: dict[str, object] | None = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": code,
                "message": message,
                "details": details or {},
                "request_id": request_id,
            }
        },
    )


async def unexpected_error_handler(request: Request, exc: Exception) -> JSONResponse:
    request_id = str(uuid4())
    logger.exception(
        "Unhandled API error",
        extra={"request_id": request_id, "path": request.url.path},
    )
    return build_error_response(
        code="INTERNAL_SERVER_ERROR",
        message="An unexpected error occurred.",
        status_code=500,
        request_id=request_id,
    )
