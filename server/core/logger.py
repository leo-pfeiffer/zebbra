import logging

from core.settings import get_settings

settings = get_settings()

if settings.ENV == "prod":
    logging.basicConfig(level=logging.ERROR)
else:
    logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("root")
