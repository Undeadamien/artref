from artref.core.config import UNSPLASH_URL
from artref.core.models import ImageAPI

route = f"{UNSPLASH_URL}/photos/random"
# note: must use the following property -> photo.links.download_location


async def fetch(query: str) -> list[ImageAPI]:
    print(query)
    return []
