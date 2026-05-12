from artref.core.models import Source
from artref.core.sources import scryfall, unsplash, wallhaven


def test_wallhaven_create_reference():
    reference = wallhaven._create_reference(
        {"id": "id", "path": "path", "source": "source"}
    )
    assert reference.source == Source.wallhaven
    assert reference.id == "id"
    assert reference.url == "path"
    assert reference.origin == "source"
    assert "" not in reference.model_dump().values()


def test_scryfall_create_reference():
    reference = scryfall._create_reference(
        {
            "id": "id",
            "image_uris": {"art_crop": "art_crop"},
            "artist": "artist",
        }
    )
    assert reference.source == Source.scryfall
    assert reference.id == "id"
    assert reference.url == "art_crop"
    assert reference.artist == "artist"
    assert "" not in reference.model_dump().values()

    reference = scryfall._create_reference(
        {
            "id": "id",
            "card_faces": [
                {"image_uris": {"art_crop": "crop_0"}, "artist": "artist_0"},
                {"image_uris": {"art_crop": "crop_1"}, "artist": "artist_1"},
            ],
        }
    )
    assert reference.source == Source.scryfall
    assert reference.id == "id"
    assert reference.url in ["crop_0", "crop_1"]
    assert reference.artist in ["artist_0", "artist_1"]
    assert (reference.url, reference.artist) in [
        ("crop_0", "artist_0"),
        ("crop_1", "artist_1"),
    ]
    assert "" not in reference.model_dump().values()


def test_unsplash_create_reference():
    reference = unsplash._create_reference(
        {
            "id": "id",
            "urls": {"regular": "path"},
            "user": {"name": "artist"},
        }
    )
    assert reference.source == Source.unsplash
    assert reference.id == "id"
    assert reference.artist == "artist"
    assert reference.url == "path"
    assert "" not in reference.model_dump().values()
