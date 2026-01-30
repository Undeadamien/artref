import os
from pathlib import Path

import aiohttp


async def download_image(session: aiohttp.ClientSession, url: str, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    async with session.get(url) as res:
        res.raise_for_status()  # todo: handle the error
        data = await res.read()
        dst.write_bytes(data)
    return dst


def require_env(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        raise RuntimeError("Missing env variable: 'key'")
    return value
