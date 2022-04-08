"""
This library contains all the functions related to playlists.
"""

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
            except TrackExistsInPlaylist as e:
                return {"error": str(e)}, 409


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


def save_p_image(file: datastructures.FileStorage, pid: str):
    """
    Saves the image of a playlist to the database.
    """
    img = Image.open(file)

    random_str = "".join(
        random.choices(string.ascii_letters + string.digits, k=5))

    img_path = pid + str(random_str) + ".webp"
    full_path = os.path.join(settings.APP_DIR, "images", "playlists", img_path)

    if file.content_type == "image/gif":
        frames = []

        for frame in ImageSequence.Iterator(img):
            frames.append(frame.copy())

        frames[0].save(full_path, save_all=True, append_images=frames[1:])
        return img_path

    img.save(full_path, "webp")

    return img_path
