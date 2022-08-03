"""
Contains all the models for objects generation and typing.
"""
from dataclasses import dataclass
from dataclasses import field
from operator import itemgetter
from typing import List

from app import helpers


@dataclass(slots=True)
class Track:
    """
    Track class
    """

    trackid: str
    title: str
    artists: list[str]
    albumartist: str
    album: str
    folder: str
    filepath: str
    length: int
    genre: str
    bitrate: int
    tracknumber: int
    discnumber: int
    albumhash: str
    date: str
    image: str
    uniq_hash: str
    copyright: str

    def __init__(self, tags):
        (
            self.title,
            self.album,
            self.albumartist,
            self.genre,
            self.albumhash,
            self.date,
            self.folder,
            self.filepath,
            self.copyright,
        ) = itemgetter(
            "title",
            "album",
            "albumartist",
            "genre",
            "albumhash",
            "date",
            "folder",
            "filepath",
            "copyright",
        )(
            tags
        )
        self.trackid = tags["_id"]["$oid"]
        self.artists = tags["artists"].split(", ")
        self.bitrate = int(tags["bitrate"])
        self.length = int(tags["length"])
        self.discnumber = int(tags["discnumber"])
        self.image = tags["albumhash"] + ".webp"
        self.tracknumber = int(tags["tracknumber"])

        self.uniq_hash = helpers.create_hash(
            "".join(self.artists), self.album, self.title
        )

    @staticmethod
    def create_unique_hash(*args):
        string = "".join(str(a) for a in args).replace(" ", "")
        return "".join([i for i in string if i.isalnum()]).lower()


@dataclass(slots=True)
class Artist:
    """
    Artist class
    """

    name: str
    image: str

    def __init__(self, name: str):
        self.name = name
        self.image = helpers.create_safe_name(name) + ".webp"


@dataclass
class Album:
    """
    Creates an album object
    """

    title: str
    artist: str
    hash: str
    date: int
    image: str
    count: int = 0
    duration: int = 0
    copyright: str = field(default="")
    is_soundtrack: bool = False
    is_compilation: bool = False
    is_single: bool = False
    colors: List[str] = field(default_factory=list)

    def __init__(self, tags):
        (
            self.title,
            self.artist,
            self.date,
            self.image,
            self.hash,
            self.copyright,
        ) = itemgetter("title", "artist", "date", "image", "hash", "copyright")(tags)

        try:
            self.colors = tags["colors"]
        except KeyError:
            self.colors = []

    @property
    def is_soundtrack(self) -> bool:
        keywords = ["motion picture", "soundtrack"]
        for keyword in keywords:
            if keyword in self.title.lower():
                return True

        return False

    @property
    def is_compilation(self) -> bool:
        return self.artist.lower() == "various artists"


@dataclass
class Playlist:
    """Creates playlist objects"""

    playlistid: str
    name: str
    tracks: List[Track]
    pretracks: list = field(init=False, repr=False)
    lastUpdated: int
    image: str
    thumb: str
    description: str = ""
    count: int = 0
    """A list of track objects in the playlist"""

    def __init__(self, data):
        self.playlistid = data["_id"]["$oid"]
        self.name = data["name"]
        self.description = data["description"]
        self.image = self.create_img_link(data["image"])
        self.thumb = self.create_img_link(data["thumb"])
        self.pretracks = data["pre_tracks"]
        self.tracks = []
        self.lastUpdated = data["lastUpdated"]
        self.count = len(self.pretracks)

    def create_img_link(self, image: str):
        if image:
            return image

        return "default.webp"

    def update_playlist(self, data: dict):
        self.name = data["name"]
        self.description = data["description"]
        self.lastUpdated = data["lastUpdated"]

        if data["image"]:
            self.image = self.create_img_link(data["image"])
            self.thumb = self.create_img_link(data["thumb"])


@dataclass
class Folder:
    name: str
    path: str
    trackcount: int
    is_sym: bool = False
    """The number of tracks in the folder"""

    def __init__(self, data) -> None:
        self.name = data["name"]
        self.path = data["path"]
        self.is_sym = data["is_sym"]
        self.trackcount = data["trackcount"]
