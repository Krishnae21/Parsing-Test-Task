import loguru
import sys

from config.settings import SETTINGS


def setup_logger() -> None:
    """Setup logger."""
    loguru.logger.remove()
    loguru.logger.add(
        sys.stdout,
        level=SETTINGS.log_level,
        colorize=True,
        enqueue=True,
        format="<level>{level}</level> | <green>{time:YYYY-MM-DD HH:mm:ss}</green>"
        " | {file.name}:{function}:{line} | {message}",
    )
