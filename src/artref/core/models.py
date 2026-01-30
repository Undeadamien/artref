from dataclasses import dataclass
from typing import Optional


@dataclass
class Reference:
    source: str
    id: str
    path: str

    artist: Optional[str] = None
    origin: Optional[str] = None  # note: original source (instagram, twitter,...)
    download_location: Optional[str] = None  # note: used by Unsplash to track downloads
    api_key: Optional[str] = None

    # todo:
    # - artist_id
    # - artist_name
