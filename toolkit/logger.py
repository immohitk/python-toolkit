"""
Logging configuration for Python Toolkit.

This module provides a centralized logger for recording
toolkit activity.
"""

import logging
from pathlib import Path


LOG_FILE = Path("toolkit.log")


def get_logger(name="python-toolkit"):
    """Return a configured logger for the toolkit."""

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(LOG_FILE)
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger