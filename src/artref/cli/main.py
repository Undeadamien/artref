import asyncio
import json
import logging
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Annotated

import aiohttp
import typer

from artref.core.config import COUNT_DEFAULT, COUNT_MAX, COUNT_MIN, get_unsplash_key
from artref.core.logging import configure_logging
from artref.core.main import fetch
from artref.core.types import Reference, Source
from artref.core.utils import download_image

app = typer.Typer(no_args_is_help=True)
configure_logging()
logger = logging.getLogger(__name__)


async def download_images(images: list[Reference], folder: Path):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for img in images:
            filepath = folder / f"{img.source.value}_{img.id}"
            tasks.append(download_image(session, img.path, filepath))

            # note: might need to be extracted if more sources need this
            if not img.download_location:
                continue
            if img.source == Source.unsplash:
                await session.get(
                    img.download_location, params={"client_id": get_unsplash_key()}
                )

        saved = await asyncio.gather(*tasks)
    return saved


def run_source(source: Source, query: str, count: int):
    timestamp = datetime.now().strftime("%y%m%d%H%M%S")
    run_dir = Path.cwd() / f"artref_{timestamp}"
    run_dir.mkdir(parents=True, exist_ok=True)

    results = asyncio.run(fetch(source, query, count))
    typer.echo(f"Fetched {len(results)} image(s) from {source}")

    if not results:
        return

    files = asyncio.run(download_images(results, run_dir))
    typer.echo(f"Downloaded {len(files)} files to {run_dir}")

    log_path = run_dir / "log.json"
    with open(log_path, "w") as file:
        json.dump([asdict(ref) for ref in results], file)


@app.command()
def scryfall(
    query: Annotated[
        str, typer.Argument(help="Syntax: 'https://scryfall.com/docs/syntax'")
    ],
    count: Annotated[int, typer.Option(min=COUNT_MIN, max=COUNT_MAX)] = COUNT_DEFAULT,
):
    """placeholder"""
    run_source(Source.scryfall, query, count)


@app.command()
def unsplash(
    query: Annotated[str, typer.Argument(help="A single search term: 'flower'")],
    count: Annotated[int, typer.Option(min=COUNT_MIN, max=COUNT_MAX)] = COUNT_DEFAULT,
):
    """placeholder"""
    run_source(Source.unsplash, query, count)


@app.command()
def wallhaven(
    query: Annotated[str, typer.Argument(help="placeholder")],
    count: Annotated[int, typer.Option(min=COUNT_MIN, max=COUNT_MAX)] = COUNT_DEFAULT,
):
    """placeholder"""
    run_source(Source.wallhaven, query, count)


def main():
    app()


if __name__ == "__main__":
    main()
