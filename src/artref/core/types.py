from typing import Awaitable, Protocol

from artref.core.models import Reference


class FetchFunction(Protocol):
    def __call__(self, query: str, count: int) -> Awaitable[list[Reference]]: ...
