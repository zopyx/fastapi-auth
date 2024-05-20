from loguru import logger as LOG  # noqa

LOG.add("fastapi-auth.log", level="DEBUG", retention="10 days")
