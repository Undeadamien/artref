import os

from typer.testing import CliRunner

from artref.cli.main import app

runner = CliRunner()


# todo: mock the response


def test_invalid_cmd(tmp_path):
    os.chdir(tmp_path)
    result = runner.invoke(app, ["noop"])
    assert result.exit_code != 0


def test_wallhaven(tmp_path):
    os.chdir(tmp_path)
    result = runner.invoke(app, ["wallhaven", "guweiz", "--count", "1"])
    assert result.exit_code == 0


def test_scryfall(tmp_path):
    os.chdir(tmp_path)
    result = runner.invoke(app, ["scryfall", "'art:magali'", "--count", "1"])
    assert result.exit_code == 0


def test_unsplash(tmp_path):
    os.chdir(tmp_path)
    result = runner.invoke(app, ["unsplash", "dawn", "--count", "1"])
    assert result.exit_code == 0
