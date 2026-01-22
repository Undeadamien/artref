from dataclasses import dataclass
from typing import Optional


@dataclass
class Reference:
    source: str
    id: str
    path: str

    artist: Optional[str] = None
    origin: Optional[str] = None  # original source, example: twitter,...
