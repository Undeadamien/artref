import asyncio
import logging
import random
from typing import Optional, cast

import aiohttp
import diskcache

from artref.core.config import CACHE_DIR, CACHE_EXPIRE, SCRYFALL_URL
from artref.core.models import Reference

logger = logging.getLogger(__name__)
cache = diskcache.Cache(CACHE_DIR)
route_search = f"{SCRYFALL_URL}/cards/search"
route_random = f"{SCRYFALL_URL}/cards/random"


# todo: find a way to handle the different layouts
# https://scryfall.com/docs/api/layouts
def createReference(data: dict) -> Optional[Reference]:
    reference = None
    try:
        reference = Reference(
            "scryfall",
            data["id"],
            data["image_uris"]["art_crop"],
            artist=data["artist"],
        )
    except:
        logging.warning("Skipping a card with an unsupported layout")
    return reference


async def fetch_search(session: aiohttp.ClientSession, params: dict):
    key = str(params)
    cached_results = await asyncio.to_thread(cache.get, key)
    if cached_results:
        return cast(dict, cached_results)  # note: silence the LSP

    try:
        async with session.get(route_search, params=params) as res:
            res.raise_for_status()
            data = await res.json()
            await asyncio.to_thread(cache.set, key, data, CACHE_EXPIRE)
            return data
    except Exception as e:
        logger.exception(e)
        return None


async def fetch_random(session: aiohttp.ClientSession, params: dict):
    try:
        async with session.get(route_random, params=params) as res:
            res.raise_for_status()
            data = await res.json()
            return data
    except Exception as e:
        logger.exception(e)
        return None


async def fetch(query: str, count: int) -> list[Reference]:
    params = {"q": query, "unique": "art"}
    results: list[Reference] = []

    # note: check the first page to determine the strategy
    async with aiohttp.ClientSession() as session:
        first_page = await fetch_search(session, params)
        if not first_page:
            return []

        has_more = first_page["has_more"]

        if not has_more:
            seen = first_page["data"]
            seen = random.sample(seen, min(count, len(seen)))
            images = [createReference(d) for d in seen]
            images = [ref for ref in images if ref]  # tmp: clear the None
            return images

        retry = 3  # tmp: fail safe
        seen = set()
        while len(seen) < count:
            if retry <= 0:  # tmp: fail safe
                break
            tasks = [fetch_random(session, params) for _ in range(count - len(seen))]
            batch = await asyncio.gather(*tasks)

            for data in batch:
                if not data or data["id"] in seen:
                    continue

                reference = createReference(data)
                if not reference:
                    retry -= 1  # tmp: fail safe
                    continue
                seen.add(data["id"])

                results.append(reference)
                if len(results) >= count:
                    break

    return results[:count]
