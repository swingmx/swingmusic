"""
This module contains mimi functions for the server.
"""
import datetime
import os
import random
import threading
import time
from typing import Dict
from typing import List

from app import models
from app import settings

app_dir = settings.APP_DIR


def background(func):
    """
    a threading decorator
    use @background above the function you want to run in the background
    """

    def background_func(*a, **kw):
        threading.Thread(target=func, args=a, kwargs=kw).start()

    return background_func


def run_fast_scandir(__dir: str,
                     ext: list,
                     full=False) -> Dict[List[str], List[str]]:
    """
    Scans a directory for files with a specific extension. Returns a list of files and folders in the directory.
    """

    subfolders = []
    files = []

    for f in os.scandir(__dir):
        if f.is_dir() and not f.name.startswith("."):
            subfolders.append(f.path)
        if f.is_file():
            if os.path.splitext(f.name)[1].lower() in ext:
                files.append(f.path)

    if full or len(files) == 0:
        for _dir in list(subfolders):
            sf, f = run_fast_scandir(_dir, ext, full=True)
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
            if (tracklist[song_num].title == song.title
                    and tracklist[song_num].album == song.album
                    and tracklist[song_num].artists == song.artists
                    and index != song_num):
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


def use_memoji():
    """
    Returns a path to a random memoji image.
    """
    path = str(random.randint(0, 20)) + ".svg"
    return "defaults/" + path


def check_artist_image(image: str) -> str:
    """
    Checks if the artist image is valid.
    """
    img_name = image.replace("/", "::") + ".webp"

    if not os.path.exists(os.path.join(app_dir, "images", "artists",
                                       img_name)):
        return use_memoji()
    else:
        return img_name


class Timer:
    begin: int = 0
    end: int = 0

    def start(self):
        self.begin = time.time()

    def stop(self):
        self.end = time.time()
        print(str(datetime.timedelta(seconds=round(self.end - self.begin))))
