"""ASGI middleware for request logging and correlation IDs."""

from __future__ import annotations

import time
import uuid
from typing import Callable

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

# Header we send back and prefer when present on incoming requests
REQUEST_ID_HEADER = "X-Request-ID"
CORRELATION_ID_HEADER = "X-Correlation-ID"


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that:
    - Assigns or propagates a correlation ID (X-Request-ID / X-Correlation-ID).
    - Binds it to request state and structlog context for the request scope.
    - Logs each request with method, path, status, duration, and correlation_id.
    - Logs errors (unhandled exceptions) with full context.
    """

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)
        self._log = structlog.get_logger(__name__)

    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        # Prefer incoming header, otherwise generate a new ID
        correlation_id = request.headers.get(
            REQUEST_ID_HEADER
        ) or request.headers.get(CORRELATION_ID_HEADER) or str(uuid.uuid4())
        request.state.correlation_id = correlation_id

        # Bind so all structlog logs in this request include correlation_id
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(correlation_id=correlation_id)

        start = time.perf_counter()
        status_code = 500  # default if we never get a response

        try:
            response = await call_next(request)
            status_code = response.status_code
            response.headers[REQUEST_ID_HEADER] = correlation_id
            return response
        except Exception as exc:
            self._log.exception(
                "request_failed",
                method=request.method,
                path=request.url.path,
                query=str(request.url.query) or None,
                error_type=type(exc).__name__,
                error=str(exc),
            )
            raise
        finally:
            duration_ms = (time.perf_counter() - start) * 1000
            self._log.info(
                "request_completed",
                method=request.method,
                path=request.url.path,
                query=str(request.url.query) or None,
                status_code=status_code,
                duration_ms=round(duration_ms, 2),
                correlation_id=correlation_id,
            )
            structlog.contextvars.clear_contextvars()


def add_correlation_id_to_response(response: Response, correlation_id: str) -> None:
    """Add correlation ID to response headers"""
    response.headers[REQUEST_ID_HEADER] = correlation_id
