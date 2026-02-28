import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Annotated

import typer

from artref.core.config import COUNT_DEFAULT, COUNT_MAX, COUNT_MIN
from artref.core.logging import configure_logging
from artref.core.main import fetch
from artref.core.session import close_session
from artref.core.types import Reference, Source
from artref.core.utils import download_image, serialize

app = typer.Typer(no_args_is_help=True)
logger = logging.getLogger(__name__)
configure_logging()

# todo: move these elsewhere
CountOption = Annotated[int, typer.Option(min=COUNT_MIN, max=COUNT_MAX)]
JsonOption = Annotated[
    bool,
    typer.Option(
        "--json",
        "-j",
        help="Print the result as a json formatted output, instead of downloading",
    ),
]


async def download_images(images: list[Reference], folder: Path):
    tasks = []
    for img in images:
        filepath = folder / f"{img.source.value}_{img.id}"
        tasks.append(download_image(img.path, filepath))
    return await asyncio.gather(*tasks)


async def run_source(source: Source, query: str, count: int, as_json: bool):
    results = await fetch(source, query, count)
    if not results:
        return

    if as_json:
        typer.echo(json.dumps([serialize(ref) for ref in results], indent=2))
        return

    timestamp = datetime.now().strftime("%y%m%d%H%M%S")
    run_dir = Path.cwd() / f"artref_{timestamp}"
    run_dir.mkdir(parents=True, exist_ok=True)
    await download_images(results, run_dir)

    log_path = run_dir / "log.json"
    with open(log_path, "w") as file:
        json.dump([serialize(ref) for ref in results], file, indent=2)


async def run(source: Source, query: str, count: int, as_json: bool):
    try:
        await run_source(source, query, count, as_json)
    finally:
        await close_session()


@app.command()
def scryfall(
    query: Annotated[str, typer.Argument(help="'https://scryfall.com/docs/syntax'")],
    count: CountOption = COUNT_DEFAULT,
    as_json: JsonOption = False,
):
    """Search random illustrations from Scryfall."""
    asyncio.run(run(Source.scryfall, query, count, as_json))


@app.command()
def unsplash(
    query: Annotated[str, typer.Argument(help="A single search term: 'flower'")],
    count: CountOption = COUNT_DEFAULT,
    as_json: JsonOption = False,
):
    """Search random photos from Unsplash."""
    asyncio.run(run(Source.unsplash, query, count, as_json))


@app.command()
def wallhaven(
    query: Annotated[str, typer.Argument(help="A single tag: 'dragon'")],
    count: CountOption = COUNT_DEFAULT,
    as_json: JsonOption = False,
):
    """Search random illustrations from Wallhaven."""
    asyncio.run(run(Source.wallhaven, query, count, as_json))


def main():
    app()


if __name__ == "__main__":
    main()
