import dataclasses
from dataclasses import dataclass

from .track import Track
from ..utils.hashing import create_hash
from swingmusic.utils.auth import get_current_userid
from ..utils.parsers import get_base_title_and_versions


@dataclass(slots=True)
class Album:
    """
    Creates an album object
    """

    albumartists: list[dict[str, str]]
    albumhash: str
    artisthashes: list[str]
    base_title: str
    color: str
    created_date: int
    date: int
    duration: int
    genres: list[dict[str, str]]
    genrehashes: list[str]
    og_title: str
    title: str
    trackcount: int
    lastplayed: int
    playcount: int
    playduration: int
    extra: dict
    pathhash: str = ""

    id: int = -1
    type: str = "album"
    image: str = ""
    _score: float = 0
    versions: list[str] = dataclasses.field(default_factory=list)
    fav_userids: list[int] = dataclasses.field(default_factory=list)
    weakhash: str = ""

    @property
    def is_favorite(self):
        return get_current_userid() in self.fav_userids

    def toggle_favorite_user(self, userid: int):
        """
        Adds or removes the given user from the list of users
        who have favorited the album.
        """
        if userid in self.fav_userids:
            self.fav_userids.remove(userid)
        else:
            self.fav_userids.append(userid)

    def __post_init__(self):
        self.image = self.albumhash + ".webp" + "?pathhash=" + self.pathhash
        self.populate_versions()
        self.weakhash = create_hash(
            self.og_title, ",".join(a["name"] for a in self.albumartists)
        )

    def populate_versions(self):
        _, self.versions = get_base_title_and_versions(self.og_title, get_versions=True)

        if "super_deluxe" in self.versions:
            self.versions.remove("deluxe")

        # at this point, we should know the type of album
        if "original" in self.versions and self.type == "soundtrack":
            self.versions.remove("original")

        self.versions = [v.replace("_", " ") for v in self.versions]

    def check_type(self, tracks: list[Track], singleTrackAsSingle: bool):
        """
        Runs all the checks to determine the type of album.
        """
        if self.is_single(tracks, singleTrackAsSingle):
            self.type = "single"
            return

        if self.is_soundtrack():
            self.type = "soundtrack"
            return

        if self.is_live_album():
            self.type = "live album"
            return

        if self.is_compilation():
            self.type = "compilation"
            return

        if self.is_ep():
            self.type = "ep"
            return

        self.type = "album"

    def is_soundtrack(self) -> bool:
        """
        Checks if the album is a soundtrack.
        """
        keywords = ["motion picture", "soundtrack"]
        for keyword in keywords:
            if keyword in self.og_title.lower():
                return True

        return False

    def is_compilation(self) -> bool:
        """
        Checks if the album is a compilation.
        """
        artists = [a["name"] for a in self.albumartists]
        artists = "".join(artists).lower()

        if "various artists" in artists:
            return True

        substrings = {
            "the essential",
            "best of",
            "greatest hits",
            "#1 hits",
            "number ones",
            "super hits",
            "collection",
            "anthology",
            "great hits",
            "biggest hits",
            "the hits",
            "the ultimate",
            "compilation",
        }

        for substring in substrings:
            if substring in self.title.lower():
                return True

        return False

    def is_live_album(self):
        """
        Checks if the album is a live album.
        """
        keywords = ["live from", "live at", "live in", "live on", "mtv unplugged"]
        for keyword in keywords:
            if keyword in self.og_title.lower():
                return True

        return False

    def is_ep(self) -> bool:
        """
        Checks if the album is an EP.
        """
        return self.title.strip().endswith(" EP")

        # TODO: check against number of tracks

    def is_single(self, tracks: list[Track], singleTrackAsSingle: bool):
        """
        Checks if the album is a single.
        """
        keywords = ["single version", "- single"]

        # show_albums_as_singles = get_flag(SessionVarKeys.SHOW_ALBUMS_AS_SINGLES)

        for keyword in keywords:
            if keyword in self.og_title.lower():
                return True

        # REVIEW: Reading from the config file in a for loop will be slow
        # TODO: Find a
        if singleTrackAsSingle and self.trackcount == 1:
            return True

        if (
            len(tracks) == 1
            and (
                create_hash(tracks[0].title) == create_hash(self.title)
                or create_hash(tracks[0].title) == create_hash(self.og_title)
            )  # if they have the same title
            # and tracks[0].track == 1
            # and tracks[0].disc == 1
            # TODO: Review -> Are the above commented checks necessary?
        ):
            return True
