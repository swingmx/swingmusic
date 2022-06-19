"""
This library contains all the functions related to albums.
"""
from pprint import pprint
import random
from typing import List

from app import helpers, instances, models
from app.lib import taglib
from tqdm import tqdm


def get_all_albums() -> List[models.Album]:
    """
    Returns a list of album objects for all albums in the database.
    """
    print("Getting all albums...")

    albums: List[models.Album] = []

    db_albums = instances.album_instance.get_all_albums()

    for album in tqdm(db_albums, desc="Creating albums"):
        aa = models.Album(album)
        albums.append(aa)

    return albums


def validate() -> None:
    """
    Creates album objects for all albums and returns
    a list of track objects
    """


def get_album_duration(album: List[models.Track]) -> int:
    """
    Gets the duration of an album.
    """

    album_duration = 0

    for track in album:
        album_duration += track.length

    return album_duration


def use_defaults() -> str:
    """
    Returns a path to a random image in the defaults directory.
    """
    path = "defaults/" + str(random.randint(0, 20)) + ".webp"
    return path


def get_album_image(track: models.Track) -> str:
    """
    Gets the image of an album.
    """

    img_p = track.albumhash + ".webp"

    success = taglib.extract_thumb(track.filepath, webp_path=img_p)

    if success:
        return img_p

    return None


class GetAlbumTracks:
    """
    Finds all the tracks that match a specific album, given the album title
    and album artist.
    """

    def __init__(self, tracklist: List[models.Track], albumhash: str) -> None:
        self.hash = albumhash
        self.tracks = tracklist
        self.tracks.sort(key=lambda x: x.albumhash)

    def __call__(self):
        tracks = helpers.UseBisection(self.tracks, "albumhash", [self.hash])()

        return tracks


def get_album_tracks(tracklist: List[models.Track], hash: str) -> List:
    return GetAlbumTracks(tracklist, hash)()


def create_album(track: models.Track) -> dict:
    """
    Generates and returns an album object from a track object.
    """
    album = {
        "title": track.album,
        "artist": track.albumartist,
        "hash": track.albumhash,
    }

    album["date"] = track.date

    img_p = get_album_image(track)

    if img_p is not None:
        album["image"] = img_p
        return album

    album["image"] = None
    return album
