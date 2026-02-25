import asyncio

import pytest

from artref.core.session import close_session, get_session


@pytest.mark.asyncio
async def test_session_concurrent():
    tasks = [asyncio.create_task(get_session()) for _ in range(20)]
    sessions = await asyncio.gather(*tasks)
    assert len(set(sessions)) == 1
    await close_session()
