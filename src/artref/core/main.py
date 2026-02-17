from artref.core.config import COUNT_DEFAULT
from artref.core.sources import scryfall, unsplash, wallhaven
from artref.core.types import FetchFunction, Source

FETCHES: dict[Source, FetchFunction] = {
    Source.scryfall: scryfall.fetch,
    Source.wallhaven: wallhaven.fetch,
    Source.unsplash: unsplash.fetch,
}


async def fetch(source: Source, query: str, count: int = COUNT_DEFAULT):
    api_fetch = FETCHES.get(source)
    if not api_fetch:
        return []

    res = await api_fetch(query, count)
    # todo: handle the case where count>len(res)
    return res
