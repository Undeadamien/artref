import asyncio
import json
import logging
from pathlib import Path
from typing import Optional

from artref.core.main import fetch
from artref.core.models import Reference, Source
from artref.core.utils import download_image

logger = logging.getLogger(__name__)


async def download_images(images: list[Reference], folder: Path):
    tasks = []
    for img in images:
        filepath = folder / f"{img.source.value}_{img.id}"
        tasks.append(download_image(img.url, filepath))

    downloaded_paths = await asyncio.gather(*tasks)

    for img, path in zip(images, downloaded_paths):
        img.local_path = path

    return downloaded_paths


async def run_fetch(
    source: Source, query: str, count: int, download_folder: Optional[Path] = None
) -> list[Reference]:
    results = await fetch(source, query, count)
    if not results:
        return []

    if download_folder:
        download_folder.mkdir(parents=True, exist_ok=True)
        await download_images(results, download_folder)

        log_path = download_folder / "log.json"
        with open(log_path, "w") as file:
            json.dump([ref.model_dump(mode="json") for ref in results], file, indent=2)

    return results
