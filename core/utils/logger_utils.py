# bible-analysis/core/utils/logger_utils.py
"""logger."""

import logging
import os

# Create logs directory if it doesn't exist
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Log file path
LOG_FILE = os.path.join(LOG_DIR, "bible_text.log")


def get_logger(logger_name):
    """Return logger with the specified name."""
    # Create a logger
    logger = logging.getLogger(logger_name)

    # Check if the logger already has handlers to avoid duplicates
    if not logger.hasHandlers():
        # Set the lowest level; individual handlers control their levels
        logger.setLevel(logging.DEBUG)

        # File handler (for saving logs to a file)
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setLevel(logging.DEBUG)  # Log all levels to file
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"  # noqa: E501
        )
        file_handler.setFormatter(file_formatter)

        # Stream handler (for console output)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)  # Log only INFO and above to console
        console_formatter = logging.Formatter("%(levelname)s - %(message)s")
        console_handler.setFormatter(console_formatter)

        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        # Prevent duplicate logs (avoid root logger propagation)
        logger.propagate = False

    return logger
