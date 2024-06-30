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

        # hack to override all the variations from unreleased files (sorry guys!)
        if self.artisthash == "5a37d5315e":
            self.name = "Juice WRLD"

    def to_json(self):
        return {
            "name": self.name,
            "artisthash": self.artisthash,
        }


@dataclass(slots=True)
class Artist:
    """
    Artist class
    """

    id: str
    name: str
    albumcount: int
    artisthash: str
    created_date: int
    date: int
    duration: int
    genres: list[dict[str, str]]
    genrehashes: list[str]
    name: str
    trackcount: int
    is_favorite: bool
    extra: dict

    image: str = ""

    def __post_init__(self):
        self.image = self.artisthash + ".webp"