import asyncio
from pathlib import Path
from pprint import pprint

import typer

from artref.core.main import fetch
from artref.core.utils import download_image

app = typer.Typer()


async def download_images(images, folder: Path):
    # todo: handle the filename prior to this
    tasks = [
        download_image(img.path, folder / f"{img.source}_{img.id}") for img in images
    ]
    saved = await asyncio.gather(*tasks)
    return saved


@app.command()
def scryfall(query: str):
    result = asyncio.run(fetch("scryfall", query))
    pprint(result)


@app.command()
def wallhaven(query: str):
    result = asyncio.run(fetch("wallhaven", query))
    files = asyncio.run(download_images(result, Path("./downloads")))
    pprint(files)


def main():
    app()
