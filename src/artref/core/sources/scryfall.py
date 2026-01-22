from artref.core.config import SCRYFALL_URL, UNSPLASH_URL
from artref.core.models import Reference

# todo: find the proper route to use
# note: json/image ?
route = f"{SCRYFALL_URL}/cards/random"  # note: easier but hacky
route = f"{SCRYFALL_URL}/cards/search"  # note: more work but cacheable


async def fetch(query: str, count: int) -> list[Reference]:
    print(query)
    return []
