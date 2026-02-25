import logging
import mimetypes
import os
from pathlib import Path
from typing import Optional

import aiohttp

from artref.core.session import get_session

logger = logging.getLogger(__name__)


async def download_image(url: str, dst: Path) -> Optional[Path]:
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        session = await get_session()
        async with session.get(url) as res:
            res.raise_for_status()
            data = await res.read()
            mime = res.headers.get("Content-Type", "")
    except aiohttp.ClientError as e:
        logger.exception(e)
        return None
    ext = mimetypes.guess_extension(mime) or ".jpg"
    dst = dst.with_suffix(ext)
    dst.write_bytes(data)
    return dst


def require_env(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        raise RuntimeError(f"Missing env variable: {key}")
    return value
