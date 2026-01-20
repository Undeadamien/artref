from pathlib import Path

import aiohttp


async def download_image(url: str, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            res.raise_for_status()  # todo: handle the error
            data = await res.read()
            dst.write_bytes(data)
    return dst
