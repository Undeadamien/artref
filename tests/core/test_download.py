import pytest

from artref.core.utils import download_image


@pytest.mark.network
@pytest.mark.asyncio
async def test_download_image(tmp_path):
    url = "https://cards.scryfall.io/art_crop/front/c/4/c4195373-e902-4fc3-aead-1f6e728dbbae.jpg"
    dst = tmp_path / "test_image"
    res = await download_image(url, dst)

    assert res is not None
    assert res.exists()
    assert res.stat().st_size > 0


@pytest.mark.network
@pytest.mark.asyncio
async def test_download_image_bad_url(tmp_path):
    url = "https://cards.scryfall.io/art_crop/bar_url"
    dst = tmp_path / "test_image"
    res = await download_image(url, dst)

    assert res is None
    assert not dst.exists()
