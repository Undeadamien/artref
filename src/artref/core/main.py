import random

from artref.core.config import DEFAULT_COUNT
from artref.core.sources import scryfall, wallhaven
from artref.core.types import FetchFunction

SOURCES: dict[str, FetchFunction] = {
    "scryfall": scryfall.fetch,
    "wallhaven": wallhaven.fetch,
}


async def fetch(source: str, query: str, count: int = DEFAULT_COUNT):
    api_fetch = SOURCES.get(source)
    if not api_fetch:
        return "The source does not exist."

    res = await api_fetch(query)

    # todo: decide how to handle len(res) < count
    res = random.sample(res, min(count, len(res)))
    return res
