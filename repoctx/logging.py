"""Small logging helper so the library and CLI share one configured logger."""

from __future__ import annotations

import logging
import os

_CONFIGURED = False


def get_logger(name: str = "repoctx") -> logging.Logger:
    """Return a package logger, configuring a stream handler once."""

    global _CONFIGURED
    logger = logging.getLogger(name)
    if not _CONFIGURED:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
        logger.addHandler(handler)
        level = os.environ.get("REPOCTX_LOG_LEVEL", "WARNING").upper()
        logger.setLevel(getattr(logging, level, logging.WARNING))
        _CONFIGURED = True
    return logger
