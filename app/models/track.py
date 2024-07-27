from dataclasses import dataclass, field

from app.utils.auth import get_current_userid


@dataclass(slots=True)
class Track:
    """
    Track class
    """

    id: int
    album: str
    albumartists: list[dict[str, str]]
    albumhash: str
    artisthashes: list[str]
    artists: list[dict[str, str]]
    bitrate: int
    copyright: str
    date: int
    disc: int
    duration: int
    filepath: str
    folder: str
    genres: list[dict[str, str]]
    genrehashes: list[str]
    last_mod: int
    og_album: str
    og_title: str
    title: str
    track: int
    trackhash: str
    extra: dict
    lastplayed: int
    playcount: int
    playduration: int

    _pos: int = 0
    _ati: str = ""
    image: str = ""
    fav_userids: list[int] = field(default_factory=list)

    @property
    def is_favorite(self):
        return get_current_userid() in self.fav_userids

    def toggle_favorite_user(self, userid: int):
        """
        Adds or removes the given user from the list of users
        who have favorited the track.
        """
        if userid in self.fav_userids:
            self.fav_userids.remove(userid)
        else:
            self.fav_userids.append(userid)

    def __post_init__(self):
        self.image = self.albumhash + ".webp"
        self.extra = {
            "disc_total": self.extra.get("disc_total", 0),
            "track_total": self.extra.get("track_total", 0),
            "samplerate": self.extra.get("samplerate", -1),
        }
