"""
This library contains all the functions related to playlists.
"""
import os
import random
import string
from datetime import datetime
from typing import List

from app import exceptions
from app import instances
from app import models
from app import settings
from app.helpers import Get, get_normalized_artists
from app.lib import trackslib
from app.logger import get_logger
from PIL import Image
from PIL import ImageSequence
from werkzeug import datastructures


TrackExistsInPlaylist = exceptions.TrackExistsInPlaylistError

logg = get_logger()


def add_track(playlistid: str, trackid: str):
    """
    Adds a track to a playlist to the database.
    """
    tt = instances.tracks_instance.get_track_by_id(trackid)

    if tt is None:
        return

    track = models.Track(tt)

    playlist = instances.playlist_instance.get_playlist_by_id(playlistid)

    track = {
        "title": track.title,
        "artists": tt["artists"],
        "album": track.album,
    }
    if track in playlist["pre_tracks"]:
        raise TrackExistsInPlaylist

    instances.playlist_instance.add_track_to_playlist(playlistid, track)


def create_thumbnail(image: any, img_path: str) -> str:
    """
    Creates a 250 x 250 thumbnail from a playlist image
    """
    thumb_path = "thumb_" + img_path
    full_thumb_path = os.path.join(settings.APP_DIR, "images", "playlists", thumb_path)

    aspect_ratio = image.width / image.height

    new_w = round(250 * aspect_ratio)

    thumb = image.resize((new_w, 250), Image.ANTIALIAS)
    thumb.save(full_thumb_path, "webp")

    return thumb_path


def save_p_image(file: datastructures.FileStorage, pid: str):
    """
    Saves the image of a playlist to the database.
    """
    img = Image.open(file)

    random_str = "".join(random.choices(string.ascii_letters + string.digits, k=5))

    img_path = pid + str(random_str) + ".webp"

    full_img_path = os.path.join(settings.APP_DIR, "images", "playlists", img_path)

    if file.content_type == "image/gif":
        frames = []

        for frame in ImageSequence.Iterator(img):
            frames.append(frame.copy())

        frames[0].save(full_img_path, save_all=True, append_images=frames[1:])
        thumb_path = create_thumbnail(img, img_path=img_path)

        return img_path, thumb_path

    img.save(full_img_path, "webp")
    thumb_path = create_thumbnail(img, img_path=img_path)

    return img_path, thumb_path


class ValidatePlaylistThumbs:
    """
    Removes all unused images in the images/playlists folder.
    """

    def __init__(self) -> None:
        images = []
        playlists = Get.get_all_playlists()

        logg.info("Validating playlist thumbnails")
        for playlist in playlists:
            if playlist.image:
                img_path = playlist.image.split("/")[-1]
                thumb_path = playlist.thumb.split("/")[-1]

                images.append(img_path)
                images.append(thumb_path)

        p_path = os.path.join(settings.APP_DIR, "images", "playlists")

        for image in os.listdir(p_path):
            if image not in images:
                os.remove(os.path.join(p_path, image))

        logg.info("Validating playlist thumbnails ... ✅")


def create_new_date():
    return datetime.now()


def create_playlist_tracks(playlist_tracks: List) -> List[models.Track]:
    """
    Creates a list of model.Track objects from a list of playlist track dicts.
    """
    tracks: List[models.Track] = []

    for t in playlist_tracks:
        track = trackslib.get_p_track(t)

        if track is not None:
            tracks.append(models.Track(track))

    return tracks


class GetPlaylistArtists:
    """
    Returns a list of artists from a list of playlist tracks.
    """

    def __init__(self, pid: str) -> None:
        self.pid = pid
        p = instances.playlist_instance.get_playlist_by_id(self.pid)
        self.tracks = create_playlist_tracks(p["pre_tracks"])

    def __call__(self):
        artists = set()

        artists = [a for t in self.tracks for a in t.artists]
        return get_normalized_artists(artists)
