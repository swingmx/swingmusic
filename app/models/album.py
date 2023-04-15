import dataclasses
from dataclasses import dataclass

from .track import Track
from .artist import Artist
from ..utils.hashing import create_hash


@dataclass(slots=True)
class Album:
    """
    Creates an album object
    """

    albumhash: str
    title: str
    albumartists: list[Artist]

    albumartisthash: str = ""
    image: str = ""
    count: int = 0
    duration: int = 0
    colors: list[str] = dataclasses.field(default_factory=list)
    date: str = ""

    is_soundtrack: bool = False
    is_compilation: bool = False
    is_single: bool = False
    is_EP: bool = False
    is_favorite: bool = False
    is_live: bool = False
    genres: list[str] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self.image = self.albumhash + ".webp"
        self.albumartisthash = "-".join(a.artisthash for a in self.albumartists)

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
            if keyword in self.title.lower():
                return True

        return False

    def check_is_compilation(self) -> bool:
        """
        Checks if the album is a compilation.
        """
        artists = [a.name for a in self.albumartists]  # type: ignore
        artists = "".join(artists).lower()

        if "various artists" in artists:
            return True

        substrings = [
            "the essential", "best of", "greatest hits", "#1 hits", "number ones", "super hits",
            "ultimate collection", "anthology", "great hits", "biggest hits", "the hits"
        ]

        for substring in substrings:
            if substring in self.title.lower():
                return True

        return False

    def check_is_live_album(self):
        """
        Checks if the album is a live album.
        """
        keywords = ["live from", "live at", "live in"]
        for keyword in keywords:
            if keyword in self.title.lower():
                return True

        return False

    def check_is_ep(self) -> bool:
        """
        Checks if the album is an EP.
        """
        return self.title.strip().endswith(" EP")

    def check_is_single(self, tracks: list[Track]):

        """
        Checks if the album is a single.
        """
        keywords = ["single version", "- single"]
        for keyword in keywords:
            if keyword in self.title.lower():
                self.is_single = True
                return

        if (
                len(tracks) == 1
                and create_hash(tracks[0].title) == create_hash(self.title)  # if they have the same title
                # and tracks[0].track == 1
                # and tracks[0].disc == 1
                # TODO: Review -> Are the above commented checks necessary?
        ):
            self.is_single = True

    def get_date_from_tracks(self, tracks: list[Track]):
        for track in tracks:
            if track.date != "Unknown":
                self.date = track.date
                break
