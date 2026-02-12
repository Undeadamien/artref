from dataclasses import asdict

from artref.core.sources import scryfall, unsplash, wallhaven


def test_wallhaven_createReference():
    reference = wallhaven.createReference(
        {
            "id": "6lm6zq",
            "path": "https://w.wallhaven.cc/full/6l/wallhaven-6lm6zq.jpg",
            "source": "https://x.com/ttguweiz/status/2016143661697036755",
        }
    )
    assert reference.source == "wallhaven"
    assert reference.id == "6lm6zq"
    assert reference.path == "https://w.wallhaven.cc/full/6l/wallhaven-6lm6zq.jpg"
    assert reference.origin == "https://x.com/ttguweiz/status/2016143661697036755"
    assert "" not in asdict(reference).values()


# todo: correct the missing aspect of scryfall.createReference
# todo: add a test for all the possible layout/structure
# note: https://scryfall.com/docs/api/layouts
def test_scryfall_createReference():
    pass


def test_unsplash_createReference():
    reference = unsplash.createReference(
        {
            "id": "OnqVBXO3Bl0",
            "urls": {
                "regular": "https://images.unsplash.com/photo-1767290718965-e862984057a9?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w4NjExMDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE3Njk3NzUyNzF8&ixlib=rb-4.1.0&q=80&w=1080",
            },
            "links": {
                "download_location": "https://api.unsplash.com/photos/OnqVBXO3Bl0/download?ixid=M3w4NjExMDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE3Njk3NzUyNzF8",
            },
            "user": {
                "name": "Kristaps Ungurs",
            },
        }
    )
    assert reference.source == "unsplash"
    assert reference.id == "OnqVBXO3Bl0"
    assert reference.artist == "Kristaps Ungurs"
    assert (
        reference.download_location
        == "https://api.unsplash.com/photos/OnqVBXO3Bl0/download?ixid=M3w4NjExMDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE3Njk3NzUyNzF8"
    )
    assert "" not in asdict(reference).values()
