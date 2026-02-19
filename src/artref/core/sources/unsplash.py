import logging

import aiohttp

from artref.core.config import UNSPLASH_URL, get_unsplash_key
from artref.core.types import Reference, Source

logger = logging.getLogger(__name__)
route = f"{UNSPLASH_URL}/photos/random"


# note: follow the API guide, must use the download_location for downloads
# > https://help.unsplash.com/en/articles/2511245-unsplash-api-guidelines
def createReference(data: dict) -> Reference:
    reference = Reference(
        Source.unsplash,
        data["id"],
        data["urls"]["regular"],
        artist=data.get("user", {}).get("name") or None,
        download_location=data.get("links", {}).get("download_location") or None,
    )
    return reference


async def fetch(query: str, count: int) -> list[Reference]:
    params = {"query": query, "client_id": get_unsplash_key(), "count": count}

    # todo: handle the pagination over 10 image and the max of 30
    async with aiohttp.ClientSession() as session:
        async with session.get(route, params=params) as res:
            data = await res.json()
            images = [createReference(d) for d in data]

            return images
