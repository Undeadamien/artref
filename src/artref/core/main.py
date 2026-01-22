from artref.core.config import DEFAULT_COUNT
from artref.core.sources import scryfall, unsplash, wallhaven
from artref.core.types import FetchFunction

SOURCES: dict[str, FetchFunction] = {
    "scryfall": scryfall.fetch,
    "wallhaven": wallhaven.fetch,
    "unsplash": unsplash.fetch,
}


async def fetch(source: str, query: str, count: int = DEFAULT_COUNT):
    api_fetch = SOURCES.get(source)
    if not api_fetch:
        return []

    res = await api_fetch(query, count)
    # todo: handle the case where count>len(res)
    return res
