import logging

from artref.core.config import COUNT_DEFAULT
from artref.core.sources import scryfall, unsplash, wallhaven
from artref.core.types import FetchFunction, Source

FETCHES: dict[Source, FetchFunction] = {
    Source.scryfall: scryfall.fetch,
    Source.wallhaven: wallhaven.fetch,
    Source.unsplash: unsplash.fetch,
}

logger = logging.getLogger(__name__)


async def fetch(source: Source, query: str, count: int = COUNT_DEFAULT):
    api_fetch = FETCHES[source]
    res = await api_fetch(query, count)
    if len(res) != count:
        logger.warning(
            "Requested %d images from '%s', got %d", count, source.value, len(res)
        )
    return res
