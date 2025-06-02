import dataclasses
from dataclasses import dataclass

from swingmusic.utils.auth import get_current_userid
from swingmusic.utils.hashing import create_hash


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
    lastplayed: int
    playcount: int
    playduration: int
    extra: dict

    id: int = -1
    image: str = ""
    _score: float = 0

    color: str = ""
    fav_userids: list[int] = dataclasses.field(default_factory=list)

    @property
    def is_favorite(self):
        return get_current_userid() in self.fav_userids

    def toggle_favorite_user(self, userid: int):
        """
        Adds or removes the given user from the list of users
        who have favorited this artist.
        """
        if userid in self.fav_userids:
            self.fav_userids.remove(userid)
        else:
            self.fav_userids.append(userid)

    def __post_init__(self):
        self.image = self.artisthash + ".webp"
