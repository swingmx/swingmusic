import json
import dataclasses
from dataclasses import dataclass

from app.utils.hashing import create_hash


@dataclass(slots=True)
class ArtistMinimal:
    """
    ArtistMinimal class
    """

    name: str
    artisthash: str = ""
    image: str = ""

    def __init__(self, name: str):
        self.name = name
        self.artisthash = create_hash(self.name, decode=True)
        self.image = self.artisthash + ".webp"


@dataclass(slots=True)
class Artist(ArtistMinimal):
    """
    Artist class
    """

    trackcount: int = 0
    albumcount: int = 0
    duration: int = 0
    colors: list[str] = dataclasses.field(default_factory=list)
    is_favorite: bool = False

    def __init__(self, name: str):
        super(Artist, self).__init__(name)
        self.colors = json.loads(str(self.colors))

    def set_trackcount(self, count: int):
        self.trackcount = count

    def set_albumcount(self, count: int):
        self.albumcount = count

    def set_duration(self, duration: int):
        self.duration = duration

    def set_colors(self, colors: list[str]):
        self.colors = colors
