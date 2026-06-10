import logging
import random
from typing import Optional

from artref.core.config import settings
from artref.core.models import Reference, Source
from artref.core.session import get_retry_client

logger = logging.getLogger(__name__)
route = f"{settings.wallhaven_url}/search"


def _create_reference(data: dict) -> Reference:
    return Reference(
        source=Source.wallhaven,
        id=data["id"],
        url=data["path"],
        origin=data.get("source") or None,
    )


async def _fetch_page(params: dict) -> Optional[dict]:
    try:
        client = await get_retry_client()
        async with client.get(route, params=params) as res:
            res.raise_for_status()
            return await res.json()
    except Exception:
        logger.exception("Wallhaven fetch failed")
        return None


async def fetch(query: str, count: int) -> list[Reference]:
    params = {"q": query, "sorting": "random"}
    data = []
    page = 1

    while len(data) < count:
        page_data = await _fetch_page({**params, "page": page})
        if not page_data or not page_data.get("data"):
            break

        data.extend(page_data["data"])

        meta = page_data.get("meta", {})
        if page >= meta.get("last_page", 1):
            break
        page += 1

        if page > 5:
            break

    data = random.sample(data, min(count, len(data)))
    return [_create_reference(d) for d in data]
