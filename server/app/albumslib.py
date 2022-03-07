from typing import List
from app import models, functions
from app import trackslib

ALBUMS: List[models.Album] = []


def create_all_albums() -> List[models.Track]:
    """
    Creates album objects for all albums and returns
    a list of track objects
    """
    albums: list[models.Album] = functions.get_all_albums()

    ALBUMS.clear()
    ALBUMS.extend(albums)
    trackslib.create_all_tracks()
    return trackslib.TRACKS


def get_album_duration(album: list) -> int:
    """
    Gets the duration of an album.
    """

    album_duration = 0

    for track in album:
        album_duration += track["length"]

    return album_duration


def get_album_image(album: list) -> str:
    """
    Gets the image of an album.
    """

    for track in album:
        img = functions.extract_thumb(track["filepath"])

        if img is not None:
            return img

    return functions.use_defaults()


def find_album(albumtitle, artist):
    for album in ALBUMS:
        if album.album == albumtitle and album.artist == artist:
            return album


def search_albums_by_name(query):
    """
    Searches albums by album name.
    """
    albums: List[models.Album] = []

    for album in ALBUMS:
        if query in album.album:
            albums.append(album)

    return albums
