from artref.core.main import FETCHES
from artref.core.types import Source


def test_validate_fetches():
    sources = {key for key in Source}
    fetches = {key for key in FETCHES.keys()}
    assert sources == fetches
