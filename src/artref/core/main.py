from typing import Awaitable, Protocol

from artref.core.config import DEFAULT_COUNT
from artref.core.sources import scryfall, wallhaven


class FetchFunction(Protocol):
    def __call__(self, query: str) -> Awaitable[list[dict]]: ...


SOURCES: dict[str, FetchFunction] = {
    "scryfall": scryfall.fetch,
    "wallhaven": wallhaven.fetch,
}


async def fetch(source: str, query: str, count: int = DEFAULT_COUNT):
    api_fetch = SOURCES.get(source)
    if not api_fetch:
        return "The source does not exist."

    print(count)
    res = await api_fetch(query)
    return res
