# Libs
import logging  # Logging
from logging.handlers import RotatingFileHandler  # Logging Handler

# Application
from core.settings import LOG_FILE  # Settings

# Logger setup
logger = logging.getLogger("openhubble_agent")
logger.setLevel(logging.INFO)

if not logger.handlers:
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler. 5MB file. 5 backups
    try:
        file_handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=5 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        )

        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.error(f"Failed to setup file logging at {LOG_FILE}: {e}")


def get_logger(name: str | None = None) -> logging.Logger:
    if name:
        return logger.getChild(name)

    return logger
