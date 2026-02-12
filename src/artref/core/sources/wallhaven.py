import logging
import random

import aiohttp

from artref.core.config import WALLHAVEN_URL
from artref.core.models import Reference

logger = logging.getLogger(__name__)
route = f"{WALLHAVEN_URL}/search"


def createReference(data: dict) -> Reference:
    reference = Reference(
        "wallhaven",
        data["id"],
        data["path"],
        origin=data.get("source") or None,
    )
    return reference


async def fetch_page(session: aiohttp.ClientSession, params: dict) -> dict | None:
    try:
        async with session.get(route, params=params) as res:
            res.raise_for_status()
            data = await res.json()
            return data
    except Exception as e:
        logger.exception(e)
        return None


async def fetch(query: str, count: int) -> list[Reference]:
    params = {"q": query, "sorting": "random"}
    data = []
    page = 1

    async with aiohttp.ClientSession() as session:
        while len(data) < count:
            page_data = await fetch_page(session, {**params, "page": page})
            if not page_data or not page_data["data"]:
                break
            data.extend(page_data["data"])
            if page >= page_data["meta"]["last_page"]:
                break
            page += 1

    data = random.sample(data, min(count, len(data)))
    images = [createReference(d) for d in data]

    return images
