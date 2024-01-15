import dataclasses
import datetime
from dataclasses import dataclass

from app.settings import SessionVarKeys, get_flag

from ..utils.hashing import create_hash
from ..utils.parsers import get_base_title_and_versions, parse_feat_from_title
from .artist import Artist
from .track import Track


@dataclass(slots=True)
class Album:
    """
    Creates an album object
    """

    albumhash: str
    title: str
    albumartists: list[Artist]

    albumartists_hashes: str = ""
    image: str = ""
    count: int = 0
    duration: int = 0
    colors: list[str] = dataclasses.field(default_factory=list)
    date: str = ""

    created_date: int = 0
    og_title: str = ""
    base_title: str = ""
    is_soundtrack: bool = False
    is_compilation: bool = False
    is_single: bool = False
    is_EP: bool = False
    is_favorite: bool = False
    is_live: bool = False

    genres: list[str] = dataclasses.field(default_factory=list)
    versions: list[str] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self.title = self.title.strip()
        self.og_title = self.title
        self.image = self.albumhash + ".webp"

        # Fetch album artists from title
        if get_flag(SessionVarKeys.EXTRACT_FEAT):
            featured, self.title = parse_feat_from_title(self.title)

            if len(featured) > 0:
                original_lower = "-".join([a.name.lower() for a in self.albumartists])
                self.albumartists.extend(
                    [Artist(a) for a in featured if a.lower() not in original_lower]
                )

                from ..store.tracks import TrackStore

                TrackStore.append_track_artists(self.albumhash, featured, self.title)

        # Handle album version data
        if get_flag(SessionVarKeys.CLEAN_ALBUM_TITLE):
            get_versions = not get_flag(SessionVarKeys.MERGE_ALBUM_VERSIONS)

            self.title, self.versions = get_base_title_and_versions(
                self.title, get_versions=get_versions
            )
            self.base_title = self.title

            if "super_deluxe" in self.versions:
                self.versions.remove("deluxe")

            if "original" in self.versions and self.check_is_soundtrack():
                self.versions.remove("original")

            self.versions = [v.replace("_", " ") for v in self.versions]
        else:
            self.base_title = get_base_title_and_versions(
                self.title, get_versions=False
            )[0]

        self.albumartists_hashes = "-".join(a.artisthash for a in self.albumartists)

    def set_colors(self, colors: list[str]):
        self.colors = colors

    def check_type(self):
        """
        Runs all the checks to determine the type of album.
        """
        self.is_soundtrack = self.check_is_soundtrack()
        if self.is_soundtrack:
            return

        self.is_live = self.check_is_live_album()
        if self.is_live:
            return

        self.is_compilation = self.check_is_compilation()
        if self.is_compilation:
            return

        self.is_EP = self.check_is_ep()

    def check_is_soundtrack(self) -> bool:
        """
        Checks if the album is a soundtrack.
        """
        keywords = ["motion picture", "soundtrack"]
        for keyword in keywords:
            if keyword in self.og_title.lower():
                return True

        return False

    def check_is_compilation(self) -> bool:
        """
        Checks if the album is a compilation.
        """
        artists = [a.name for a in self.albumartists]
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
            "compilation"
        }

        for substring in substrings:
            if substring in self.title.lower():
                return True

        return False

    def check_is_live_album(self):
        """
        Checks if the album is a live album.
        """
        keywords = ["live from", "live at", "live in", "live on", "mtv unplugged"]
        for keyword in keywords:
            if keyword in self.og_title.lower():
                return True

        return False

    def check_is_ep(self) -> bool:
        """
        Checks if the album is an EP.
        """
        return self.title.strip().endswith(" EP")

        # TODO: check against number of tracks

    def check_is_single(self, tracks: list[Track]):
        """
        Checks if the album is a single.
        """
        keywords = ["single version", "- single"]

        show_albums_as_singles = get_flag(SessionVarKeys.SHOW_ALBUMS_AS_SINGLES)

        for keyword in keywords:
            if keyword in self.og_title.lower():
                self.is_single = True
                return

        if show_albums_as_singles and len(tracks) == 1:
            self.is_single = True
            return

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
            self.is_single = True

    def get_date_from_tracks(self, tracks: list[Track]):
        """
        Gets the date of the album its tracks.

        Args:
            tracks (list[Track]): The tracks of the album.
        """
        if self.date:
            return

        dates = (int(t.date) for t in tracks if t.date)
        try:
            self.date = datetime.datetime.fromtimestamp(min(dates)).year
        except:
            self.date = datetime.datetime.now().year

    def set_count(self, count: int):
        self.count = count

    def set_duration(self, duration: int):
        self.duration = duration

    def set_created_date(self, created_date: int):
        self.created_date = created_date
