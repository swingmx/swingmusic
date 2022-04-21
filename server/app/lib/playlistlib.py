"""
This library contains all the functions related to playlists.
"""
from datetime import datetime
import os
import random
import string

from app import api
from app import exceptions
from app import instances
from app import models
from app import settings
from app.lib import trackslib
from PIL import Image
from PIL import ImageSequence
from progress.bar import Bar
from werkzeug import datastructures

TrackExistsInPlaylist = exceptions.TrackExistsInPlaylist


def add_track(playlistid: str, trackid: str):
    """
    Adds a track to a playlist in the api.PLAYLISTS dict and to the database.
    """
    for playlist in api.PLAYLISTS:
        if playlist.playlistid == playlistid:
            tt = trackslib.get_track_by_id(trackid)

            track = {
                "title": tt.title,
                "artists": tt.artists,
                "album": tt.album,
            }

            try:
                playlist.add_track(track)
                instances.playlist_instance.add_track_to_playlist(
                    playlistid, track)
                return
            except TrackExistsInPlaylist as error:
                raise error


def get_playlist_tracks(pid: str):
    for p in api.PLAYLISTS:
        if p.playlistid == pid:
            return p.tracks


def create_all_playlists():
    """
    Gets all playlists from the database.
    """
    playlists = instances.playlist_instance.get_all_playlists()

    _bar = Bar("Creating playlists", max=len(playlists))

    for playlist in playlists:
        api.PLAYLISTS.append(models.Playlist(playlist))

        _bar.next()
    _bar.finish()

    validate_images()


def create_thumbnail(image: any, img_path: str) -> str:
    """
    Creates a 250 x 250 thumbnail from a playlist image
    """
    thumb_path = "thumb_" + img_path
    full_thumb_path = os.path.join(
        settings.APP_DIR, "images", "playlists", thumb_path)

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

    random_str = "".join(random.choices(
        string.ascii_letters + string.digits, k=5))

    img_path = pid + str(random_str) + ".webp"

    full_img_path = os.path.join(
        settings.APP_DIR, "images", "playlists", img_path)

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


def validate_images():
    """
    Removes all unused images in the images/playlists folder.
    """
    images = []

    for playlist in api.PLAYLISTS:
        if playlist.image:
            img_path = playlist.image.split("/")[-1]
            thumb_path = playlist.thumb.split("/")[-1]

            images.append(img_path)
            images.append(thumb_path)

    p_path = os.path.join(settings.APP_DIR, "images", "playlists")

    for image in os.listdir(p_path):
        if image not in images:
            os.remove(os.path.join(p_path, image))


def create_new_date():
    return datetime.now()
