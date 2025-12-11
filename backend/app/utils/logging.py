"""Centralized logging configuration."""

import json
import logging
import logging.config
import sys
from datetime import datetime
from typing import Any, Dict

from app.core.config import settings


class JSONFormatter(logging.Formatter):
    """Formatter that outputs log records as JSON objects."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        # Add extra fields from log call (e.g., logger.info("msg", extra={"user_id": 123}))
        if hasattr(record, "extras"):
            log_entry.update(record.extras)
        else:
            # Include any attributes not in default LogRecord
            for key, value in record.__dict__.items():
                if key not in (
                    "name", "msg", "args", "levelname", "levelno", "pathname", "filename",
                    "module", "lineno", "funcName", "created", "msecs", "relativeCreated",
                    "thread", "threadName", "processName", "process", "exc_info", "exc_text",
                    "stack_info", "message", "levelname", "extras"
                ):
                    log_entry[key] = value

        return json.dumps(log_entry, ensure_ascii=False)


def setup_logging() -> None:
    """Configure the root logger based on environment settings."""
    log_level = logging.DEBUG if settings.debug else logging.INFO

    if settings.log_json:
        # Structured JSON logging for production
        formatter = JSONFormatter()
    else:
        # Human-readable logging for development
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)-8s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(handler)

    # Reduce noise from external libraries
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("celery").setLevel(logging.INFO)
    logging.getLogger("urllib3").setLevel(logging.WARNING)


# Convenience logger for application modules
logger = logging.getLogger("housemusic")