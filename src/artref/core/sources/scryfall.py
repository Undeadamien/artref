from artref.core.config import SCRYFALL_URL, UNSPLASH_URL
from artref.core.models import ImageAPI

# todo: find the proper route to use
# note: json/image ?
route = f"{SCRYFALL_URL}/cards/random"  # note: easier but hacky
route = f"{SCRYFALL_URL}/cards/search"  # note: more work but cacheable


async def fetch(query: str) -> list[ImageAPI]:
    print(query)
    return []
