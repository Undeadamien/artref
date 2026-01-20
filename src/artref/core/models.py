from typing import Optional


class ImageAPI:
    def __init__(self, source: str, id: str, *, artist: Optional[str] = None):
        self.source: str = source
        self.id: str = id

        self.artist: Optional[str] = artist

    def __repr__(self):
        return repr(vars(self))
