import logging

import aiohttp

from artref.core.config import UNSPLASH_KEY, UNSPLASH_URL
from artref.core.models import Reference

logger = logging.getLogger(__name__)
route = f"{UNSPLASH_URL}/photos/random"


# note: follow the API guide, must use the download_location for downloads
# > https://help.unsplash.com/en/articles/2511245-unsplash-api-guidelines
def createReference(data: dict) -> Reference:
    reference = Reference(
        "unsplash",
        data["id"],
        data["urls"]["regular"],
        artist=data["user"]["name"],
        download_location=data["links"]["download_location"],
    )
    return reference


async def fetch(query: str, count: int) -> list[Reference]:
    params = {"query": query, "client_id": UNSPLASH_KEY, "count": count}

    # todo: handle the pagination over 10 image and the max of 30
    async with aiohttp.ClientSession() as session:
        async with session.get(route, params=params) as res:
            data = await res.json()
            images = [createReference(d) for d in data]

            return images
