import asyncio
from typing import cast

import aiohttp
import diskcache

URL = "https://wallhaven.cc/api/v1/search"
EXPIRE = 24 * 60 * 60

cache = diskcache.Cache("./cache")


async def fetch_page(params: dict) -> dict | None:
    key = str(params)
    cached_results = await asyncio.to_thread(cache.get, key)
    if cached_results:
        return cast(dict, cached_results)  # note: to silence the LSP

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(URL, params=params) as res:
                res.raise_for_status()
                data = await res.json()
                await asyncio.to_thread(cache.set, key, data, EXPIRE)
                return data
        except Exception as e:
            print("Error fetching page:", e)
            return None


async def fetch() -> list[dict]:
    data = []
    params = {"q": "guweiz"}

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

    return data


if __name__ == "__main__":
    all_data = asyncio.run(fetch())
    print(f"Fetched {len(all_data)} wallpapers")
