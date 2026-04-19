"""Structlog logging configuration."""

import logging
import sys
from typing import Any

import structlog


def configure_logging(level: int = logging.INFO) -> None:
    """Configure JSON structured logging.

    Args:
        level: Python logging level.
    """
    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=level)
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(component: str, **kwargs: Any) -> structlog.stdlib.BoundLogger:
    """Get a structured logger with a component binding.

    Args:
        component: Logical subsystem emitting logs.
        **kwargs: Additional bound context.

    Returns:
        Bound structlog logger.
    """
    logger = structlog.get_logger().bind(component=component)
    if kwargs:
        logger = logger.bind(**kwargs)
    return logger
