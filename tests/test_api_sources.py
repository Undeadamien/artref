from artref.api.main import list_sources


def test_list_sources():
    expected = {"scryfall", "wallhaven", "unsplash"}
    res = set(list_sources())
    assert res == expected
