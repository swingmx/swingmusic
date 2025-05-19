from dataclasses import asdict, dataclass, field

from swingmusic.config import UserConfig
from swingmusic.utils.auth import get_current_userid
from swingmusic.utils.hashing import create_hash
from swingmusic.utils.parsers import (
    clean_title,
    get_base_title_and_versions,
    parse_feat_from_title,
    remove_prod,
    split_artists,
)


@dataclass(slots=True)
class Track:
    """
    Track class
    """

    id: int
    album: str
    albumartists: list[dict[str, str]]
    albumhash: str
    artists: list[dict[str, str]]
    bitrate: int
    copyright: str
    date: int
    disc: int
    duration: int
    filepath: str
    folder: str
    genres: str | list[dict[str, str]]
    last_mod: int
    title: str
    track: int
    trackhash: str
    extra: dict
    lastplayed: int
    playcount: int
    playduration: int

    config: UserConfig
    og_album: str = ""
    og_title: str = ""
    artisthashes: list[str] = field(default_factory=list)
    genrehashes: list[str] = field(default_factory=list)
    weakhash: str = ""

    _pos: int = 0
    _ati: str = ""
    image: str = ""
    _score: float = 0
    explicit: bool = False
    fav_userids: list[int] = field(default_factory=list)

    @property
    def is_favorite(self):
        return get_current_userid() in self.fav_userids

    @property
    def pathhash(self):
        return create_hash(self.folder)

    def toggle_favorite_user(self, userid: int):
        """
        Toggles the favorite status of the track for a given user.

        Args:
            userid (int): The ID of the user toggling the favorite status.
        """
        if userid in self.fav_userids:
            self.fav_userids.remove(userid)
        else:
            self.fav_userids.append(userid)

    def __post_init__(self):
        """
        Performs post-initialization processing on the track object.
        This includes setting original values, processing artists and genres,
        and removing duplicate artists.
        """
        self.og_title = self.title
        self.og_album = self.album
        self.folder = self.folder + "/"
        self.weakhash = create_hash(self.title, self.artists)
        explicit_tag = self.extra.get("explicit", ["0"])
        self.explicit = int(explicit_tag[0]) == 1

        self.image = self.albumhash + ".webp" + "?pathhash=" + self.pathhash
        # self.extra = {
        #     "disc_total": self.extra.get("disc_total", 0),
        #     "track_total": self.extra.get("track_total", 0),
        #     "samplerate": self.extra.get("samplerate", -1),
        # }

        self.split_artists()
        self.map_with_config()
        self.process_genres()

        # Remove duplicates from artists and albumartists
        seen_artists = set()
        self.artists = [
            d
            for d in self.artists
            if tuple(d.items()) not in seen_artists
            and not seen_artists.add(tuple(d.items()))
        ]

        seen_albumartists = set()
        self.albumartists = [
            d
            for d in self.albumartists
            if tuple(d.items()) not in seen_albumartists
            and not seen_albumartists.add(tuple(d.items()))
        ]

        self.recreate_trackhash()
        self.config = None

    def split_artists(self):
        """
        Splits the artists and albumartists based on the given separators,
        and updates the artisthashes.
        """

        def split(artists: str):
            return [
                {"name": a, "artisthash": create_hash(a, decode=True)}
                for a in split_artists(artists, config=self.config)
            ]

        self.artists = split(self.artists)
        self.albumartists = split(self.albumartists)
        self.artisthashes = [a["artisthash"] for a in self.artists]

    def map_with_config(self):
        """
        Applies various transformations to the track's title and album
        based on the user's configuration settings.
        """
        new_title = self.title

        # Extract featured artists
        if self.config.extractFeaturedArtists:
            feat, new_title = parse_feat_from_title(self.title, self.config)
            feat = [
                {"name": f, "artisthash": create_hash(f, decode=True)} for f in feat
            ]
            feat = [f for f in feat if f["artisthash"] not in self.artisthashes]
            self.artists.extend(feat)
            self.artisthashes.extend([f["artisthash"] for f in feat])

            # Update album title for singles
            # ie. album: "Title (feat. Artist)"
            #     title: "Title (feat. Artist)"
            # becomes: album: "Title", title: "Title"
            if self.og_album == self.og_title:
                self.album = new_title

        # Clean track title
        if self.config.removeProdBy:
            new_title = remove_prod(new_title)

        # if self.title == new_title:
        #     self.album = new_title

        if self.config.removeRemasterInfo:
            new_title = clean_title(new_title)

        self.title = new_title

        # Clean album title
        if self.config.cleanAlbumTitle:
            self.album, _ = get_base_title_and_versions(self.album, get_versions=False)

        if self.config.mergeAlbums:
            self.albumhash = create_hash(
                self.album, *(a["name"] for a in self.albumartists)
            )

    def process_genres(self):
        """
        Processes and standardizes the genre information for the track.
        """
        if self.genres:
            src_genres: str = self.genres

            src_genres = src_genres.lower()
            # separators = {"/", ";", "&"}
            separators = set(self.config.genreSeparators)

            contains_rnb = "r&b" in src_genres
            contains_rock = "rock & roll" in src_genres

            if contains_rnb:
                src_genres = src_genres.replace("r&b", "RnB")

            if contains_rock:
                src_genres = src_genres.replace("rock & roll", "rock")

            for s in separators:
                src_genres = src_genres.replace(s, ",")

            genres_list: list[str] = src_genres.split(",")
            self.genres = [
                {"name": g.strip(), "genrehash": create_hash(g.strip())}
                for g in genres_list
            ]
            self.genrehashes = [g["genrehash"] for g in self.genres]

    def recreate_trackhash(self):
        """
        Recreates the trackhash based on the current title, album, and artist information.
        """
        self.trackhash = create_hash(
            self.title, self.album, *(artist["name"] for artist in self.artists)
        )

    def copy(self):
        return Track(**{**asdict(self), "config": UserConfig()})
