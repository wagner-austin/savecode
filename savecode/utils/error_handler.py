"""
savecode/utils/error_handler.py - Helper functions for error logging and aggregation.
Provides a unified function to log messages and record them in the shared context.
"""

from typing import Dict
import logging

def log_and_record_error(message: str, context: Dict[str, any], logger: logging.Logger, level: str = "error") -> None:
    """
    Logs a message using the provided logger at the specified level and appends the message to the context's errors list.
    
    :param message: The message to log and record.
    :param context: The shared context dictionary.
    :param logger: The logger to use for logging.
    :param level: The logging level: "error", "warning", or "info" (default is "error").
    """
    level = level.lower()
    if level == "error":
        logger.error(message)
    elif level == "warning":
        logger.warning(message)
    elif level == "info":
        logger.info(message)
    else:
        logger.debug(message)
    context.setdefault('errors', []).append(message)
