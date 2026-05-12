from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

from artref.core.config import settings


class Source(str, Enum):
    scryfall = "scryfall"
    wallhaven = "wallhaven"
    unsplash = "unsplash"


class Reference(BaseModel):
    source: Source
    id: str
    url: str
    artist: Optional[str] = None
    origin: Optional[str] = None
    local_path: Optional[Path] = None


class FetchParams(BaseModel):
    source: Source
    query: str
    count: int = Field(
        settings.count_default, ge=settings.count_min, le=settings.count_max
    )
