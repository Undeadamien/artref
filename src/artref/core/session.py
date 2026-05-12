import asyncio
from typing import Optional

import aiohttp
from aiohttp_retry import ExponentialRetry, RetryClient

_session: Optional[aiohttp.ClientSession] = None
_retry_client: Optional[RetryClient] = None
_session_lock = asyncio.Lock()
_retry_lock = asyncio.Lock()

USER_AGENT = "ArtRef/0.1.0 (+https://github.com/undeadamien/artref)"


async def get_session() -> aiohttp.ClientSession:
    global _session
    if _session is None or _session.closed:
        async with _session_lock:
            if _session is None or _session.closed:
                headers = {"User-Agent": USER_AGENT}
                _session = aiohttp.ClientSession(headers=headers)
    return _session


async def get_retry_client() -> RetryClient:
    global _retry_client
    if _retry_client is None:
        async with _retry_lock:
            if _retry_client is None:
                session = await get_session()
                retry_options = ExponentialRetry(
                    attempts=3, statuses={429, 500, 502, 503, 504}, start_timeout=0.5
                )
                _retry_client = RetryClient(
                    client_session=session, retry_options=retry_options
                )
    return _retry_client


async def close_session():
    global _session, _retry_client
    async with _retry_lock:
        if _retry_client:
            await _retry_client.close()
            _retry_client = None

    async with _session_lock:
        if _session and not _session.closed:
            await _session.close()
            _session = None
