import logging

from aiocache import cached

from artref.core.config import settings
from artref.core.models import Source
from artref.core.sources import scryfall, unsplash, wallhaven
from artref.core.types import FetchFunction

FETCHES: dict[Source, FetchFunction] = {
    Source.scryfall: scryfall.fetch,
    Source.wallhaven: wallhaven.fetch,
    Source.unsplash: unsplash.fetch,
}

logger = logging.getLogger(__name__)


@cached(
    ttl=settings.cache_expire,
    key_builder=lambda _, source, query, count: f"{source}:{query}:{count}",
)
async def fetch(source: Source, query: str, count: int = settings.count_default):
    api_fetch = FETCHES[source]
    res = await api_fetch(query, count)

    if len(res) != count:
        logger.warning(
            "Requested %d images from '%s', got %d", count, source.value, len(res)
        )
    return res
