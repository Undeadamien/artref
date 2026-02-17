from dataclasses import dataclass
from enum import Enum
from typing import Awaitable, Optional, Protocol

import pydantic


class Source(str, Enum):
    scryfall = "scryfall"
    wallhaven = "wallhaven"
    unsplash = "unsplash"


@dataclass
class Reference:
    source: Source
    id: str
    path: str

    artist: Optional[str] = None
    origin: Optional[str] = None  # note: original source (instagram, twitter,...)
    download_location: Optional[str] = None  # note: used by Unsplash to track downloads

    # todo:
    # - artist_id
    # - artist_name


@pydantic.dataclasses.dataclass
class ImageResponse(Reference):
    pass


class FetchFunction(Protocol):
    def __call__(self, query: str, count: int) -> Awaitable[list[Reference]]: ...
