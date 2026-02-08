import asyncio
import logging
from pathlib import Path

import aiohttp
import typer

from artref.core.config import UNSPLASH_KEY
from artref.core.logging import configure_logging
from artref.core.main import SOURCES, fetch
from artref.core.models import Reference
from artref.core.utils import download_image

app = typer.Typer()
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


def run_source(source: str, query: str):
    results = asyncio.run(fetch(source, query))
    logger.info("Fetched %s image from %s", len(results), source)
    files = asyncio.run(download_images(results, Path.cwd()))
    logger.info("Downloaded %s files to %s", len(files), Path.cwd())


for source in SOURCES:
    app.command(name=source)(lambda query, src=source: run_source(src, query))


def main():
    app()


if __name__ == "__main__":
    main()
