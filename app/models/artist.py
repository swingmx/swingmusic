import dataclasses
import json
from dataclasses import dataclass

from app.utils.hashing import create_hash


@dataclass(slots=True)
class Artist:
    """
    Artist class
    """

    name: str
    artisthash: str = ""
    image: str = ""
    trackcount: int = 0
    albumcount: int = 0
    duration: int = 0
    colors: list[str] = dataclasses.field(default_factory=list)
    is_favorite: bool = False

    def __post_init__(self):
        self.artisthash = create_hash(self.name, decode=True)
        self.image = self.artisthash + ".webp"
        self.colors = json.loads(str(self.colors))


@dataclass(slots=True)
class ArtistMinimal:
    """
    ArtistMinimal class
    """

    name: str
    artisthash: str = ""
    image: str = ""

    def __post_init__(self):
        self.artisthash = create_hash(self.name, decode=True)
        self.image = self.artisthash + ".webp"
