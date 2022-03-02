"""
This module contains mimi functions for the server.
"""

import os
import threading
import time
from typing import List
import requests
import colorgram

from io import BytesIO

from PIL import Image

from app import instances
from app import functions
from app import watchdoge
from app import models

home_dir = os.path.expanduser("~") + "/"
app_dir = os.path.join(home_dir, ".musicx")
LAST_FM_API_KEY = "762db7a44a9e6fb5585661f5f2bdf23a"


def background(func):
    """
    a threading decorator
    use @background above the function you want to run in the background
    """

    def background_func(*a, **kw):
        threading.Thread(target=func, args=a, kwargs=kw).start()

    return background_func


@background
def reindex_tracks():
    """
    Checks for new songs every 5 minutes.
    """
    flag = False

    while flag is False:
        functions.populate()
        functions.populate_images()
        time.sleep(300)


@background
def start_watchdog():
    """
    Starts the file watcher.
    """
    watchdoge.watch.run()


def run_fast_scandir(_dir: str, ext: list):
    """
    Scans a directory for files with a specific extension. Returns a list of files and folders in the directory.
    """

    subfolders = []
    files = []

    for f in os.scandir(_dir):
        if f.is_dir() and not f.name.startswith("."):
            subfolders.append(f.path)
        if f.is_file():
            if os.path.splitext(f.name)[1].lower() in ext:
                files.append(f.path)

    for _dir in list(subfolders):
        sf, f = run_fast_scandir(_dir, ext)
        subfolders.extend(sf)
        files.extend(f)

    return subfolders, files


def remove_duplicates(tracklist: List[models.Track]) -> List[models.Track]:
    """
    Removes duplicates from a list. Returns a list without duplicates.
    """

    song_num = 0

    while song_num < len(tracklist) - 1:
        for index, song in enumerate(tracklist):
            if (
                tracklist[song_num].title == song.title
                and tracklist[song_num].album == song.album
                and tracklist[song_num].artists == song.artists
                and index != song_num
            ):
                tracklist.remove(song)

        song_num += 1

    return tracklist


def save_image(url: str, path: str) -> None:
    """
    Saves an image from an url to a path.
    """

    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.save(path, "JPEG")


def is_valid_file(filename: str) -> bool:
    """
    Checks if a file is valid. Returns True if it is, False if it isn't.
    """

    if filename.endswith(".flac") or filename.endswith(".mp3"):
        return True
    else:
        return False


def create_config_dir() -> None:
    """
    Creates the config directory if it doesn't exist.
    """

    _home_dir = os.path.expanduser("~")
    config_folder = os.path.join(_home_dir, app_dir)

    dirs = ["", "images", "images/defaults", "images/artists", "images/thumbnails"]

    for _dir in dirs:
        path = os.path.join(config_folder, _dir)

        try:
            os.makedirs(path)
        except FileExistsError:
            pass

        os.chmod(path, 0o755)


def get_all_songs() -> List[models.Track]:
    """
    Gets all songs under the ~/ directory.
    """
    print("Getting all songs...")

    tracks: list[models.Track] = []

    for track in instances.songs_instance.get_all_songs():
        try:
            os.chmod(os.path.join(track["filepath"]), 0o755)
        except FileNotFoundError:
            instances.songs_instance.remove_song_by_filepath(track["filepath"])

        tracks.append(functions.create_track_class(track))

    return tracks


def extract_colors(image) -> list:
    colors = sorted(colorgram.extract(image, 2), key=lambda c: c.hsl.h)

    formatted_colors = []

    for color in colors:
        color = f"rgb({color.rgb.r}, {color.rgb.g}, {color.rgb.b})"
        formatted_colors.append(color)

    return formatted_colors


def get_album_duration(album: List[models.Track]) -> int:
    """
    Gets the duration of an album.
    """

    album_duration = 0

    for track in album:
        album_duration += track.length

    return album_duration