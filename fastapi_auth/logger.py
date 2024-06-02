from loguru import logger as LOG  # noqa

from .auth_config import AUTH_SETTINGS

LOG.add(
    AUTH_SETTINGS.log_filename,
    level="DEBUG",
    retention="10 days",
)
