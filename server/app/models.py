"""
Contains all the models for objects generation and typing.
"""

from dataclasses import dataclass
from datetime import date
from typing import List
from app import api
from app import settings


@dataclass
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

    def __init__(self, tags):
        self.trackid = tags["_id"]["$oid"]
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


@dataclass
class Album:
    """
    Album class
    """

    album: str
    artist: str
    count: int
    duration: int
    date: int
    artistimage: str
    image: str

    def __init__(self, tags):
        self.album = tags["album"]
        self.artist = tags["artist"]
        self.count = tags["count"]
        self.duration = tags["duration"]
        self.date = tags["date"]
        self.artistimage = settings.IMG_ARTIST_URI + tags["artistimage"]
        self.image = settings.IMG_THUMB_URI + tags["image"]


def create_playlist_tracks(playlist_tracks: List) -> List[Track]:
    """
    Creates a list of model.Track objects from a list of playlist track dicts.
    """
    tracks: List[Track] = []

    for t in playlist_tracks:
        for track in api.TRACKS:
            if (
                track.title == t["title"]
                and track.artists == t["artists"]
                and track.album == t["album"]
            ):
                tracks.append(track)

    return tracks


@dataclass
class Playlist:
    """Creates playlist objects"""

    playlistid: str
    name: str
    description: str
    image: str
    tracks: List[Track]
    count: int
    lastUpdated: int
    """A list of track objects in the playlist"""

    def __init__(self, data):
        self.playlistid = data["_id"]["$oid"]
        self.name = data["name"]
        self.description = data["description"]
        self.image = ""
        self.tracks = create_playlist_tracks(data["tracks"])
        self.count = len(data["tracks"])
        self.lastUpdated = data["lastUpdated"]



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
