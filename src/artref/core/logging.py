import logging

from artref.core.config import settings


def configure_logging():
    logging.basicConfig(
        level=getattr(logging, settings.logging_level.upper(), logging.WARNING)
    )
