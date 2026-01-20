import asyncio
from typing import cast

import aiohttp
import diskcache

from artref.core.config import CACHE_DIR, CACHE_EXPIRE, WALLHAVEN_URL
from artref.core.models import ImageAPI

cache = diskcache.Cache(CACHE_DIR)


async def fetch_page(params: dict) -> dict | None:
    key = str(params)
    cached_results = await asyncio.to_thread(cache.get, key)
    if cached_results:
        return cast(dict, cached_results)  # note: to silence the LSP

    # todo: implement a retry logic
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(WALLHAVEN_URL, params=params) as res:
                res.raise_for_status()
                data = await res.json()
                await asyncio.to_thread(cache.set, key, data, CACHE_EXPIRE)
                return data
        except Exception as e:
            print("Error:", e)
            return None


async def fetch(query: str) -> list[ImageAPI]:
    data = []
    params = {"q": query}

    first_page = await fetch_page(params)
    if not first_page:
        return []

    data.extend(first_page["data"])
    last_page = first_page["meta"]["last_page"]

    tasks = [fetch_page({**params, "page": i}) for i in range(2, last_page + 1)]
    results = await asyncio.gather(*tasks)

    for res in results:
        if res:
            data.extend(res["data"])

    images = []
    for d in data:
        image = ImageAPI("wallhaven", d["id"])
        images.append(image)

    return images
