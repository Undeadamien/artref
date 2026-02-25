import logging
import random
from typing import Optional

import aiohttp

from artref.core.config import WALLHAVEN_URL
from artref.core.session import get_session
from artref.core.types import Reference, Source

logger = logging.getLogger(__name__)
route = f"{WALLHAVEN_URL}/search"


def _create_reference(data: dict) -> Reference:
    reference = Reference(
        Source.wallhaven,
        data["id"],
        data["path"],
        origin=data.get("source") or None,
    )
    return reference


async def _fetch_page(params: dict) -> Optional[dict]:
    try:
        session = await get_session()
        async with session.get(route, params=params) as res:
            res.raise_for_status()
            data = await res.json()
            return data
    except aiohttp.ClientError as e:
        logger.exception(e)
        return None


async def fetch(query: str, count: int) -> list[Reference]:
    params = {"q": query, "sorting": "random"}
    data = []
    page = 1

    while len(data) < count:
        page_data = await _fetch_page({**params, "page": page})
        if not page_data or not page_data["data"]:
            break
        data.extend(page_data["data"])
        if page >= page_data["meta"]["last_page"]:
            break
        page += 1

    data = random.sample(data, min(count, len(data)))
    images = [_create_reference(d) for d in data]

    return images
