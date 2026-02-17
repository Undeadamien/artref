from dataclasses import asdict

from artref.core.sources import scryfall, unsplash, wallhaven
from artref.core.types import Source


def test_wallhaven_createReference():
    reference = wallhaven.createReference(
        {
            "id": "id",
            "path": "path",
            "source": "source",
        }
    )
    assert reference.source == Source.wallhaven
    assert reference.id == "id"
    assert reference.path == "path"
    assert reference.origin == "source"
    assert "" not in asdict(reference).values()


def test_scryfall_createReference():
    reference = scryfall.createReference(
        {
            "id": "id",
            "image_uris": {"art_crop": "art_crop"},
            "artist": "artist",
        }
    )
    assert reference.source == Source.scryfall
    assert reference.id == "id"
    assert reference.path == "art_crop"
    assert reference.artist == "artist"
    assert "" not in asdict(reference).values()

    reference = scryfall.createReference(
        {
            "id": "id",
            "card_faces": [
                {"image_uris": {"art_crop": "0"}, "artist": "0"},
                {"image_uris": {"art_crop": "1"}, "artist": "1"},
            ],
        }
    )
    assert reference.source == Source.scryfall
    assert reference.id == "id"
    assert reference.path in ["0", "1"]
    assert reference.artist in ["0", "1"]
    assert reference.path == reference.artist  # note: might need some change
    assert "" not in asdict(reference).values()


def test_unsplash_createReference():
    reference = unsplash.createReference(
        {
            "id": "id",
            "urls": {"regular": "path"},
            "links": {"download_location": "download_location"},
            "user": {"name": "artist"},
        }
    )
    assert reference.source == Source.unsplash
    assert reference.id == "id"
    assert reference.artist == "artist"
    assert reference.path == "path"
    assert reference.download_location == "download_location"
    assert "" not in asdict(reference).values()
