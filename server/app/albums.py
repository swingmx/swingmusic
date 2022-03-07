from typing import List
from app import models, instances, functions

all_albums: List[models.Album] = []


def create_all_albums() -> List[models.Album]:
    """Creates album objects for all albums"""
    albums: list[models.Album] = []

    for album in instances.album_instance.get_all_albums():
        albums.append(models.Album(album))

    return albums


def get_album_duration(album: List[models.Track]) -> int:
    """
    Gets the duration of an album.
    """

    album_duration = 0

    for track in album:
        try:
            album_duration += track.length
        except AttributeError:
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
