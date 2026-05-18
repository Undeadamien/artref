import asyncio
import logging
import random

from artref.core.config import settings
from artref.core.models import Reference, Source
from artref.core.session import get_retry_client

logger = logging.getLogger(__name__)
route_search = f"{settings.scryfall_url}/cards/search"
route_random = f"{settings.scryfall_url}/cards/random"


def _create_reference(data: dict) -> Reference:
    if "image_uris" in data:
        return Reference(
            source=Source.scryfall,
            id=data["id"],
            url=data.get("image_uris", {}).get("art_crop"),
            artist=data.get("artist") or None,
        )
    face = random.choice(data["card_faces"])
    return Reference(
        source=Source.scryfall,
        id=f"{data['id']}",
        url=face.get("image_uris", {}).get("art_crop"),
        artist=face.get("artist") or data.get("artist") or None,
    )


async def _fetch_search(params: dict):
    try:
        client = await get_retry_client()
        async with client.get(route_search, params=params) as res:
            res.raise_for_status()
            return await res.json()
    except Exception:
        logger.exception("Scryfall search failed")
        return None


async def _fetch_random(params: dict):
    try:
        client = await get_retry_client()
        async with client.get(route_random, params=params) as res:
            res.raise_for_status()
            return await res.json()
    except Exception:
        logger.exception("Scryfall random fetch failed")
        return None


async def fetch(query: str, count: int) -> list[Reference]:
    params = {"q": query, "unique": "art"}

    first_page = await _fetch_search(params)

    if not first_page or "data" not in first_page:
        return []

    has_more = first_page["has_more"]

    if not has_more:
        seen = first_page["data"]
        seen = random.sample(seen, min(count, len(seen)))
        return [_create_reference(d) for d in seen]

    results: list[Reference] = []
    seen_ids = set()

    max_attempts = count * 2
    attempts = 0

    while len(results) < count and attempts < max_attempts:
        tasks = [_fetch_random(params) for _ in range(count - len(results))]
        batch = await asyncio.gather(*tasks, return_exceptions=True)

        for data in batch:
            attempts += 1
            if isinstance(data, BaseException) or not data:
                continue

            if data["id"] in seen_ids:
                continue

            results.append(_create_reference(data))
            seen_ids.add(data["id"])
            if len(results) >= count:
                break

    return results
