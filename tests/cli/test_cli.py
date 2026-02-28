import os

import pytest
from typer.testing import CliRunner

from artref.cli.main import app

runner = CliRunner()


# todo: mock the response


@pytest.mark.network
@pytest.mark.parametrize(
    "source,query",
    [("wallhaven", "guweiz"), ("scryfall", "artist:magali"), ("unsplash", "tree")],
)
@pytest.mark.parametrize("count", [1, 2])
def test_cmd_valid(tmp_path, source, query, count):
    os.chdir(tmp_path)
    result = runner.invoke(app, [source, query, "--count", count])
    assert result.exit_code == 0
    dirs = list(tmp_path.iterdir())
    assert len(dirs) == 1
    run_dir = dirs[0]
    assert run_dir.name.startswith("artref_")
    files = list(run_dir.iterdir())
    images = [f for f in files if f.suffix != ".json"]
    log = [f for f in files if f.suffix == ".json"]
    assert len(images) == count
    assert len(log) == 1
    assert log[0].stat().st_size > 0
    assert all(map(lambda x: x.stat().st_size > 0, images))


@pytest.mark.network
@pytest.mark.parametrize(
    "source,query",
    [("wallhaven", "guweiz"), ("scryfall", "artist:magali"), ("unsplash", "tree")],
)
@pytest.mark.parametrize("count", [0, 999])
def test_cmd_invalid(tmp_path, source, query, count):
    os.chdir(tmp_path)
    result = runner.invoke(app, [source, query, "--count", count])
    assert result.exit_code != 0
