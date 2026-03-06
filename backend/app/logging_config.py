"""Structured logging configuration: JSON output and correlation ID support."""

from __future__ import annotations

import logging
import sys
from typing import Any

import structlog

CORRELATION_ID_KEY = "correlation_id"


def configure_logging(
    *,
    json_logs: bool = True,
    log_level: str = "INFO",
) -> None:
    """
    Configure structlog and standard logging for the application.
    """
    shared_processors: list[Any] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
        structlog.processors.format_exc_info,
    ]

    if json_logs:
        processors = shared_processors + [structlog.processors.JSONRenderer()]
    else:
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer(colors=True),
        ]

    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper(), logging.INFO),
    )


def get_logger(*args: Any, **kwargs: Any) -> structlog.BoundLogger:
    """Return a structlog logger (use after configure_logging)."""
    return structlog.get_logger(*args, **kwargs)
