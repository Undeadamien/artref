import asyncio
import json
import logging
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Annotated

import aiohttp
import typer

from artref.core.config import COUNT_DEFAULT, COUNT_MAX, COUNT_MIN, UNSPLASH_KEY
from artref.core.logging import configure_logging
from artref.core.main import fetch
from artref.core.models import Reference
from artref.core.utils import download_image

app = typer.Typer(no_args_is_help=True)
configure_logging()
logger = logging.getLogger(__name__)


async def download_images(images: list[Reference], folder: Path):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for img in images:
            filepath = folder / f"{img.source}_{img.id}"
            tasks.append(download_image(session, img.path, filepath))

            # note: might need to be extracted if more sources need this
            if not img.download_location:
                continue
            if img.source == "unsplash":
                await session.get(
                    img.download_location, params={"client_id": UNSPLASH_KEY}
                )

        saved = await asyncio.gather(*tasks)
    return saved


def run_source(source: str, query: str, count: int):
    results = asyncio.run(fetch(source, query, count))
    typer.echo(f"Fetched {len(results)} image from {source}")
    files = asyncio.run(download_images(results, Path.cwd()))
    typer.echo(f"Downloaded {len(files)} files to {Path.cwd()}")
    filepath = Path.cwd() / f"artref_{datetime.now().strftime('%y%m%d%H%M%S')}.json"
    if not results:
        return
    with open(filepath, "w") as file:
        json.dump([asdict(ref) for ref in results], file)
    typer.echo(f"Log saved: '{filepath}'")


@app.command()
def scryfall(
    query: Annotated[
        str, typer.Argument(help="Syntax: 'https://scryfall.com/docs/syntax'")
    ],
    count: Annotated[int, typer.Option(min=COUNT_MIN, max=COUNT_MAX)] = COUNT_DEFAULT,
):
    """placeholder"""
    run_source("scryfall", query, count)


@app.command()
def unsplash(
    query: Annotated[str, typer.Argument(help="A single search term: 'flower'")],
    count: Annotated[int, typer.Option(min=COUNT_MIN, max=COUNT_MAX)] = COUNT_DEFAULT,
):
    """placeholder"""
    run_source("unsplash", query, count)


@app.command()
def wallhaven(
    query: Annotated[str, typer.Argument(help="placeholder")],
    count: Annotated[int, typer.Option(min=COUNT_MIN, max=COUNT_MAX)] = COUNT_DEFAULT,
):
    """placeholder"""
    run_source("wallhaven", query, count)


def main():
    app()


if __name__ == "__main__":
    main()
