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


@dataclass(slots=True)
class Artist(ArtistMinimal):
    """
    Artist class
    """

    name: str = ""
    trackcount: int = 0
    albumcount: int = 0
    duration: int = 0
    colors: list[str] = dataclasses.field(default_factory=list)
    is_favorite: bool = False
    created_date: float = 0.0

    def __post_init__(self):
        super(Artist, self).__init__(self.name)

    def set_trackcount(self, count: int):
        self.trackcount = count

    def set_albumcount(self, count: int):
        self.albumcount = count

    def set_duration(self, duration: int):
        self.duration = duration

    def set_colors(self, colors: list[str]):
        self.colors = colors

    def set_created_date(self, created_date: float):
        self.created_date = created_date
