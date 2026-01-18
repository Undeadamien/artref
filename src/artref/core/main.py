from artref.core.sources import scryfall, wallhaven


def fetch(source: str):
    if source == "scryfall":
        return scryfall.fetch()
    if source == "wallhaven":
        return wallhaven.fetch()
    return "The source does not exist."
