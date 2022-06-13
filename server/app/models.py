"""
Contains all the models for objects generation and typing.
"""
from dataclasses import dataclass, field
from typing import List

from app import helpers
from app.exceptions import TrackExistsInPlaylist


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
    image: str
    tracknumber: int
    disknumber: int
    albumhash: str

    def __init__(self, tags):
        try:
            self.trackid = tags["_id"]["$oid"]
        except KeyError:
            print("No id")
            print(tags)

        self.title = tags["title"]
        self.artists = tags["artists"].split(", ")
        self.albumartist = tags["albumartist"]
        self.album = tags["album"]
        self.folder = tags["folder"]
        self.filepath = tags["filepath"]
        self.genre = tags["genre"]
        self.bitrate = int(tags["bitrate"])
        self.length = int(tags["length"])
        self.disknumber = int(tags["disknumber"])
        self.albumhash = tags["albumhash"]

        try:
            self.image = tags["image"]
        except KeyError:
            print(tags)

        try:
            self.tracknumber = int(tags["tracknumber"])
        except ValueError:
            self.tracknumber = 1


@dataclass(slots=True)
class Artist:
    """
    Artist class
    """

    artistid: str
    name: str
    image: str

    def __init__(self, tags):
        self.artistid = tags["_id"]["$oid"]
        self.name = tags["name"]
        self.image = tags["image"]


@dataclass
class Album:
    """
    Album class
    """

    title: str
    artist: str
    date: int
    image: str
    hash: str
    count: int = 0
    duration: int = 0
    is_soundtrack: bool = False
    is_compilation: bool = False
    is_single: bool = False

    def __init__(self, tags):
        self.title = tags["title"]
        self.artist = tags["artist"]
        self.date = tags["date"]
        self.image = tags["image"]

        try:
            self.hash = tags["albumhash"]
        except KeyError:
            self.hash = helpers.create_album_hash(self.title, self.artist)

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

    def update_count(self):
        self.count = len(self.pretracks)

    def add_track(self, track):
        if track not in self.pretracks:
            self.pretracks.append(track)
            self.update_count()
            self.lastUpdated = helpers.create_new_date()
        else:
            raise TrackExistsInPlaylist("Track already exists in playlist")

    def update_desc(self, desc):
        self.description = desc

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
