import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Annotated

import typer

from artref.core.config import settings
from artref.core.logging import configure_logging
from artref.core.models import Source
from artref.core.service import run_fetch
from artref.core.session import close_session

app = typer.Typer(no_args_is_help=True)
logger = logging.getLogger(__name__)
configure_logging()

CountOption = Annotated[
    int, typer.Option(min=settings.count_min, max=settings.count_max)
]
JsonOption = Annotated[
    bool,
    typer.Option(
        "--json",
        "-j",
        help="Print the result as a json formatted output, instead of downloading",
    ),
]


async def run(source: Source, query: str, count: int, as_json: bool):
    try:
        download_folder = None
        if not as_json:
            timestamp = datetime.now().strftime("%y%m%d%H%M%S")
            download_folder = Path.cwd() / f"artref_{timestamp}"

        results = await run_fetch(source, query, count, download_folder)

        if not results:
            return

        if as_json:
            typer.echo(
                json.dumps([ref.model_dump(mode="json") for ref in results], indent=2)
            )
    finally:
        await close_session()


@app.command()
def scryfall(
    query: Annotated[str, typer.Argument(help="'https://scryfall.com/docs/syntax'")],
    count: CountOption = settings.count_default,
    as_json: JsonOption = False,
):
    """Search random illustrations from Scryfall."""
    asyncio.run(run(Source.scryfall, query, count, as_json))


@app.command()
def unsplash(
    query: Annotated[str, typer.Argument(help="A single search term: 'flower'")],
    count: CountOption = settings.count_default,
    as_json: JsonOption = False,
):
    """Search random photos from Unsplash."""
    asyncio.run(run(Source.unsplash, query, count, as_json))


@app.command()
def wallhaven(
    query: Annotated[str, typer.Argument(help="A single tag: 'dragon'")],
    count: CountOption = settings.count_default,
    as_json: JsonOption = False,
):
    """Search random illustrations from Wallhaven."""
    asyncio.run(run(Source.wallhaven, query, count, as_json))


def main():
    app()


if __name__ == "__main__":
    main()
