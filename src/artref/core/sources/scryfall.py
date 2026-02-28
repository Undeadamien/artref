import asyncio
import logging
import random
from typing import cast

import aiohttp
import diskcache

from artref.core.config import CACHE_DIR, CACHE_EXPIRE, SCRYFALL_URL
from artref.core.session import get_session
from artref.core.types import Reference, Source

logger = logging.getLogger(__name__)
cache = diskcache.Cache(CACHE_DIR)
route_search = f"{SCRYFALL_URL}/cards/search"
route_random = f"{SCRYFALL_URL}/cards/random"


# todo: improve the way 'multi-faced' cards are handled
def _create_reference(data: dict) -> Reference:
    if "image_uris" in data:
        return Reference(
            Source.scryfall,
            data["id"],
            data.get("image_uris", {}).get("art_crop"),
            artist=data.get("artist") or None,
        )
    face = random.choice(data["card_faces"])
    return Reference(
        Source.scryfall,
        f"{data['id']}",
        face.get("image_uris", {}).get("art_crop"),
        artist=face.get("artist") or data.get("artist") or None,
    )


async def _fetch_search(params: dict):
    key = str(params)
    cached_results = await asyncio.to_thread(cache.get, key)
    if cached_results:
        return cast(dict, cached_results)  # note: silence the LSP

    try:
        session = await get_session()
        async with session.get(route_search, params=params) as res:
            res.raise_for_status()
            data = await res.json()
            await asyncio.to_thread(cache.set, key, data, CACHE_EXPIRE)
            return data
    except aiohttp.ClientError as e:
        logger.exception(e)
        return None


async def _fetch_random(params: dict):
    try:
        session = await get_session()
        async with session.get(route_random, params=params) as res:
            res.raise_for_status()
            data = await res.json()
            return data
    except aiohttp.ClientError as e:
        logger.exception(e)
        return None


async def fetch(query: str, count: int) -> list[Reference]:
    params = {"q": query, "unique": "art"}
    results: list[Reference] = []

    # note: check the first page to determine the strategy
    first_page = await _fetch_search(params)
    if not first_page:
        return []

    has_more = first_page["has_more"]

    if not has_more:
        seen = first_page["data"]
        seen = random.sample(seen, min(count, len(seen)))
        images = [_create_reference(d) for d in seen]
        images = [ref for ref in images if ref]
        return images

    seen = set()
    while len(seen) < count:
        tasks = [_fetch_random(params) for _ in range(count - len(seen))]
        batch = await asyncio.gather(*tasks)

        for data in batch:
            if not data or data["id"] in seen:
                continue

            reference = _create_reference(data)
            seen.add(data["id"])

            results.append(reference)
            if len(results) >= count:
                break

    return results[:count]
