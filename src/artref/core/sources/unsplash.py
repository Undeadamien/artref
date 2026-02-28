import logging

import aiohttp

from artref.core.config import UNSPLASH_URL, get_unsplash_key
from artref.core.session import get_session
from artref.core.types import Reference, Source

logger = logging.getLogger(__name__)
route = f"{UNSPLASH_URL}/photos/random"


def _create_reference(data: dict) -> Reference:
    reference = Reference(
        Source.unsplash,
        data["id"],
        data["urls"]["regular"],
        artist=data.get("user", {}).get("name") or None,
    )
    return reference


async def fetch(query: str, count: int) -> list[Reference]:
    params = {"query": query, "client_id": get_unsplash_key(), "count": count}

    # todo: handle the pagination over 10 image and the max of 30
    try:
        session = await get_session()
        async with session.get(route, params=params) as res:
            res.raise_for_status()
            data = await res.json()
    except aiohttp.ClientError as e:
        logger.exception(e)
        return []

    return [_create_reference(d) for d in data]
