import dataclasses
from dataclasses import dataclass

from swingmusic.store.plays import PlayStats, PlayStore
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
    extra: dict

    id: int = -1
    image: str = ""
    _score: float = 0

    color: str = ""
    blurhash: str = ""
    fav_userids: list[int] = dataclasses.field(default_factory=list)

    @property
    def plays(self) -> PlayStats:
        """
        The current user's play stats for this artist.
        """
        return PlayStore.get(get_current_userid(), "artist", self.artisthash)

    @property
    def playcount(self) -> int:
        return self.plays.playcount

    @property
    def playduration(self) -> int:
        return self.plays.playduration

    @property
    def lastplayed(self) -> int:
        return self.plays.lastplayed

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

    def set_image_version(self, version: int | None):
        """
        Points the image at an uploaded version, or at the default image when None.
        """
        self.image = self.artisthash + ".webp" + (f"?v={version}" if version else "")
