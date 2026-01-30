import asyncio
from pathlib import Path
from pprint import pprint

import aiohttp
import typer

from artref.core.logging import configure_logging
from artref.core.main import fetch
from artref.core.models import Reference
from artref.core.utils import download_image

app = typer.Typer()


async def download_images(images: list[Reference], folder: Path):
    # todo: handle the filename prior to this
    async with aiohttp.ClientSession() as session:
        tasks = []
        for img in images:
            filepath = folder / f"{img.source}_{img.id}"  # todo: a proper extension
            tasks.append(download_image(session, img.path, filepath))

            # todo: extract this part
            if img.download_location and img.api_key:
                session.get(img.download_location, params={"client_id": img.api_key})

        saved = await asyncio.gather(*tasks)
    return saved


@app.command()
def scryfall(query: str):
    result = asyncio.run(fetch("scryfall", query))
    files = asyncio.run(download_images(result, Path.cwd()))
    pprint(result)
    pprint(files)


@app.command()
def wallhaven(query: str):
    result = asyncio.run(fetch("wallhaven", query))
    files = asyncio.run(download_images(result, Path.cwd()))
    pprint(result)
    pprint(files)


@app.command()
def unsplash(query: str):
    result = asyncio.run(fetch("unsplash", query))
    files = asyncio.run(download_images(result, Path.cwd()))
    pprint(result)
    pprint(files)


def main():
    configure_logging()
    app()
