"""
This module contains mimi functions for the server.
"""

import os
import threading
import time
from typing import List
import requests

from io import BytesIO

from PIL import Image

from app import instances
from app import functions
from app import watchdoge

home_dir = os.path.expanduser('~') + '/'
app_dir = os.path.join(home_dir, '.musicx')
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
def check_for_new_songs():
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
    watchdoge.watch.run()


def run_fast_scandir(_dir: str, ext: list):
    """
    Scans a directory for files with a specific extension. Returns a list of files and folders in the directory.
    """

    subfolders = []
    files = []

    for f in os.scandir(_dir):
        if f.is_dir() and not f.name.startswith('.'):
            subfolders.append(f.path)
        if f.is_file():
            if os.path.splitext(f.name)[1].lower() in ext:
                files.append(f.path)

    for _dir in list(subfolders):
        sf, f = run_fast_scandir(_dir, ext)
        subfolders.extend(sf)
        files.extend(f)

    return subfolders, files


def remove_duplicates(array: list) -> list:
    """
    Removes duplicates from a list. Returns a list without duplicates.
    """

    song_num = 0

    while song_num < len(array) - 1:
        for index, song in enumerate(array):
            if array[song_num].title == song.title and \
                    array[song_num].album == song.album and \
                    array[song_num].artists == song.artists and \
                    index != song_num:
                array.remove(song)

        song_num += 1

    return array


def save_image(url: str, path: str) -> None:
    """
    Saves an image from an url to a path.
    """

    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.save(path, 'JPEG')


def is_valid_file(filename: str) -> bool:
    """
    Checks if a file is valid. Returns True if it is, False if it isn't.
    """

    if filename.endswith('.flac') or filename.endswith('.mp3'):
        return True
    else:
        return False


def create_config_dir() -> None:
    """
    Creates the config directory if it doesn't exist.
    """

    _home_dir = os.path.expanduser('~')
    config_folder = os.path.join(_home_dir, app_dir)

    dirs = ["", "images", "images/defaults",
            "images/artists", "images/thumbnails"]

    for _dir in dirs:
        path = os.path.join(config_folder, _dir)

        try:
            os.makedirs(path)
        except FileExistsError:
            pass

        os.chmod(path, 0o755)


def get_all_songs() -> List:
    """
    Gets all songs under the ~/ directory.
    """
    print("Getting all songs...")
    tracks = []

    for track in instances.songs_instance.get_all_songs():
        try:
            os.chmod(os.path.join(track["filepath"]), 0o755)
        except FileNotFoundError:
            instances.songs_instance.remove_song_by_filepath(track['filepath'])

        tracks.append(functions.create_track_class(track))

    return tracks
