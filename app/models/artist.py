import dataclasses
import json
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

    def __post_init__(self):
        super(Artist, self).__init__(self.name)
        self.colors = json.loads(str(self.colors))

    def set_colors(self, colors: list[str]):
        self.colors = colors

# TODO: Use inheritance to create the classes in this file.
