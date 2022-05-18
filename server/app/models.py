"""
Contains all the models for objects generation and typing.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import List

from app import api
from app.exceptions import TrackExistsInPlaylist
from app import helpers


@dataclass(slots=True)
class Track:
    """
    Track class
    """

    trackid: str
    title: str
    artists: str
    albumartist: str
    album: str
    folder: str
    filepath: str
    length: int
    genre: str
    bitrate: int
    image: str
    tracknumber: int
    discnumber: int
    albumhash: str

    def __init__(self, tags):
        try:
            self.trackid = tags["_id"]["$oid"]
        except KeyError:
            print(tags)

        self.title = tags["title"]
        self.artists = tags["artists"].split(", ")
        self.albumartist = tags["albumartist"]
        self.album = tags["album"]
        self.folder = tags["folder"]
        self.filepath = tags["filepath"]
        self.length = tags["length"]
        self.genre = tags["genre"]
        self.bitrate = tags["bitrate"]
        self.image = tags["image"]
        self.tracknumber = tags["tracknumber"]
        self.discnumber = tags["discnumber"]
        self.albumhash = tags["albumhash"]


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

    def __init__(self, tags):
        self.title = tags["title"]
        self.artist = tags["artist"]
        self.date = tags["date"]
        self.image = tags["image"]
        self.hash = helpers.create_album_hash(self.title, self.artist)

        try:
            self.hash = tags["albumhash"]
        except KeyError:
            self.hash = helpers.create_album_hash(self.title, self.artist)


def get_p_track(ptrack):
    for track in api.TRACKS:
        if (
            track.title == ptrack["title"]
            and track.artists == ptrack["artists"]
            and ptrack["album"] == track.album
        ):
            return track


def create_playlist_tracks(playlist_tracks: List) -> List[Track]:
    """
    Creates a list of model.Track objects from a list of playlist track dicts.
    """
    tracks: List[Track] = []

    for t in playlist_tracks:
        track = get_p_track(t)
        if track is not None:
            tracks.append(track)

    return tracks


@dataclass
class Playlist:
    """Creates playlist objects"""

    playlistid: str
    name: str
    tracks: List[Track]
    _pre_tracks: list = field(init=False, repr=False)
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
        self._pre_tracks = data["pre_tracks"]
        self.tracks = []
        self.lastUpdated = data["lastUpdated"]
        self.count = len(self._pre_tracks)

    def get_tracks(self) -> List[Track]:
        """
        Generates and returns Track objects from pre_tracks
        """
        return create_playlist_tracks(self._pre_tracks)

    def create_img_link(self, image: str):
        if image:
            return image

        return "default.webp"

    def update_count(self):
        self.count = len(self._pre_tracks)

    def add_track(self, track):
        if track not in self._pre_tracks:
            self._pre_tracks.append(track)
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
    """The number of tracks in the folder"""

    def __init__(self, data) -> None:
        self.name = data["name"]
        self.path = data["path"]
        self.trackcount = data["trackcount"]
