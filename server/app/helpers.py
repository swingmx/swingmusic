"""
This module contains mimi functions for the server.
"""

import os
import threading
from typing import List
import colorgram

from app import models

home_dir = os.path.expanduser("~") + "/"
app_dir = os.path.join(home_dir, ".musicx")


def background(func):
    """
    a threading decorator
    use @background above the function you want to run in the background
    """

    def background_func(*a, **kw):
        threading.Thread(target=func, args=a, kwargs=kw).start()

    return background_func


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


# def save_image(url: str, path: str) -> None:
#     """
#     Saves an image from an url to a path.
#     """

#     response = requests.get(url)
#     img = Image.open(BytesIO(response.content))
#     img.save(path, "JPEG")


def is_valid_file(filename: str) -> bool:
    """
    Checks if a file is valid. Returns True if it is, False if it isn't.
    """

    if filename.endswith(".flac") or filename.endswith(".mp3"):
        return True
    else:
        return False


def extract_image_colors(image) -> list:
    """Extracts 2 of the most dominant colors from an image."""
    try:
        colors = sorted(colorgram.extract(image, 2), key=lambda c: c.hsl.h)
    except OSError:
        return []

    formatted_colors = []

    for color in colors:
        color = f"rgb({color.rgb.r}, {color.rgb.g}, {color.rgb.b})"
        formatted_colors.append(color)

    return formatted_colors


def check_artist_image(image: str) -> str:
    """
    Checks if the artist image is valid.
    """
    img_name = image.replace("/", "::") + ".webp"

    if not os.path.exists(os.path.join(app_dir, "images", "artists", img_name)):
        return "http://10.5.8.182:8900/images/artists/0.webp"
    else:
        return ("http://10.5.8.182:8900/images/artists/" + img_name,)
