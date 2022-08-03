"""
This library contains all the functions related to albums.
"""
import os
import random
from dataclasses import dataclass
from typing import List

from app import helpers
from app import instances
from app import models
from app.lib import taglib
from app.logger import logg
from app.settings import THUMBS_PATH
from tqdm import tqdm


@dataclass
class Thumbnail:
    filename: str


class RipAlbumImage:
    """
    Rips a thumbnail for the given album hash.
    """

    def __init__(self, hash: str) -> None:
        tracks = instances.tracks_instance.find_tracks_by_hash(hash)
        tracks = [models.Track(track) for track in tracks]

        for track in tracks:
            ripped = taglib.extract_thumb(track.filepath, hash + ".webp")

            if ripped:
                break


class ValidateAlbumThumbs:
    @staticmethod
    def remove_obsolete():
        """
        Removes unreferenced thumbnails from the thumbnails folder.
        """
        entries = os.scandir(THUMBS_PATH)
        entries = [entry for entry in entries if entry.is_file()]

        albums = helpers.Get.get_all_albums()
        thumbs = [Thumbnail(album.hash + ".webp") for album in albums]

        for entry in tqdm(entries, desc="Validating thumbnails"):
            e = helpers.UseBisection(thumbs, "filename", [entry.name])()

            if e is None:
                os.remove(entry.path)
                break

            if os.path.getsize(entry.path) == 0:
                os.remove(entry.path)

    @staticmethod
    def find_lost_thumbnails():
        """
        Re-rip lost album thumbnails
        """
        entries = os.scandir(THUMBS_PATH)
        entries = [Thumbnail(entry.name) for entry in entries if entry.is_file()]

        albums = helpers.Get.get_all_albums()
        thumbs = [(album.hash + ".webp") for album in albums]

        def rip_image(t_hash: str):
            e = helpers.UseBisection(entries, "filename", [t_hash])()[0]

            if e is None:
                hash = t_hash.replace(".webp", "")
                RipAlbumImage(hash)

        logg.info("Ripping lost album thumbnails")
        # with ThreadPoolExecutor() as pool:
        #     i = pool.map(rip_image, thumbs)
        #     [a for a in i]
        # ⚠️ empty lists are sent to the useBisection function as the source list.
        for thumb in thumbs:
            rip_image(thumb)

        logg.info("Ripping lost album thumbnails ... ✅")

    def __init__(self) -> None:
        self.remove_obsolete()
        self.find_lost_thumbnails()


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
        "copyright": track.copyright,
    }

    album["date"] = track.date

    img_p = get_album_image(track)

    if img_p is not None:
        album["image"] = img_p
        return album

    album["image"] = None
    return album
