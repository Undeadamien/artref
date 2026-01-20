from typing import Awaitable, Protocol

from artref.core.models import ImageAPI


class FetchFunction(Protocol):
    def __call__(self, query: str) -> Awaitable[list[ImageAPI]]: ...
