import json
from dataclasses import dataclass


@dataclass(slots=True)
class Playlist:
    """Creates playlist objects"""

    id: int
    artisthashes: str | list[str]
    banner_pos: int
    has_gif: str | bool
    image: str
    last_updated: str
    name: str
    trackhashes: str | list[str]

    thumb: str = ""
    count: int = 0
    duration: int = 0

    def __post_init__(self):
        self.trackhashes = json.loads(str(self.trackhashes))
        self.artisthashes = json.loads(str(self.artisthashes))

        self.count = len(self.trackhashes)
        self.has_gif = bool(int(self.has_gif))

        if self.image is not None:
            self.thumb = "thumb_" + self.image
        else:
            self.image = "None"
            self.thumb = "None"
