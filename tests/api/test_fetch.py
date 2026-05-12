import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from artref.api.main import app

client = TestClient(app)


@pytest.mark.network
def test_fetch_endpoint_no_download():
    response = client.get(
        "/fetch", params={"source": "scryfall", "query": "artist:magali", "count": 1}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["source"] == "scryfall"
    assert data[0]["local_path"] is None


@pytest.mark.network
def test_fetch_endpoint_with_download(tmp_path):
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        response = client.get(
            "/fetch",
            params={
                "source": "scryfall",
                "query": "artist:magali",
                "count": 1,
                "download": "true",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

        dirs = [
            d for d in tmp_path.iterdir() if d.is_dir() and d.name.startswith("artref_")
        ]
        assert len(dirs) == 1
        run_dir = dirs[0]

        files = list(run_dir.iterdir())
        assert any(f.name == "log.json" for f in files)
        assert any(f.suffix in [".jpg", ".png", ".jpeg"] for f in files)

        assert data[0]["local_path"] is not None
        assert Path(data[0]["local_path"]).exists()
    finally:
        os.chdir(original_cwd)


@pytest.mark.network
def test_fetch_invalid_source():
    response = client.get("/fetch", params={"source": "invalid", "query": "test"})
    assert response.status_code == 422


@pytest.mark.network
def test_fetch_not_found():
    response = client.get(
        "/fetch",
        params={
            "source": "scryfall",
            "query": "thisqueryshouldneverfindanythingever",
            "count": 1,
        },
    )
    assert response.status_code == 404
