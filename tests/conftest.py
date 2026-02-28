import pytest

from artref.core.session import close_session


@pytest.fixture(autouse=True)
async def cleanup():
    yield
    await close_session()
