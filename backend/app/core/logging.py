"""Centralized logging configuration."""

import logging
import sys
from typing import Any
from app.core.config import settings


class SecretMaskingFormatter(logging.Formatter):
    """Log formatter that masks sensitive keys and tokens."""

    def format(self, record: logging.LogRecord) -> str:
        formatted = super().format(record)
        if settings.MONDAY_API_TOKEN and settings.MONDAY_API_TOKEN in formatted:
            formatted = formatted.replace(settings.MONDAY_API_TOKEN, "***MASKED_MONDAY_TOKEN***")
        if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY in formatted:
            formatted = formatted.replace(settings.GEMINI_API_KEY, "***MASKED_GEMINI_KEY***")
        return formatted


def setup_logger(name: str = "skylark_bi") -> logging.Logger:
    """Configures and returns a logger instance."""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = SecretMaskingFormatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


logger = setup_logger()
