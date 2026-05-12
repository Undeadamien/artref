import logging

from artref.core.config import settings
from artref.core.models import Reference, Source
from artref.core.session import get_retry_client

logger = logging.getLogger(__name__)
route = f"{settings.unsplash_url}/photos/random"


def _create_reference(data: dict) -> Reference:
    return Reference(
        source=Source.unsplash,
        id=data["id"],
        url=data["urls"]["regular"],
        artist=data.get("user", {}).get("name") or None,
    )


async def fetch(query: str, count: int) -> list[Reference]:
    try:
        params = {"query": query, "client_id": settings.get_unsplash_key(), "count": count}
        client = await get_retry_client()
        async with client.get(route, params=params) as res:
            res.raise_for_status()
            data = await res.json()

            if not isinstance(data, list):
                data = [data]

            return [_create_reference(d) for d in data]
    except Exception:
        logger.exception("Unsplash fetch failed")
        return []
