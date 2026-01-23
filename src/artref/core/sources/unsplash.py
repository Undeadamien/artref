import logging

from artref.core.config import UNSPLASH_URL
from artref.core.models import Reference

logger = logging.getLogger(__name__)
route = f"{UNSPLASH_URL}/photos/random"
# note: must use the following property -> photo.links.download_location


async def fetch(query: str, count: int) -> list[Reference]:
    logger.info(query, count)
    return []
