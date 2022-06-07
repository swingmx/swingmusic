"""
This module contains mini functions for the server.
"""
import os
import random
import threading
import time
from datetime import datetime
from typing import Any
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


def run_fast_scandir(__dir: str, full=False) -> Dict[List[str], List[str]]:
    """
    Scans a directory for files with a specific extension. Returns a list of files and folders in the directory.
    """

    subfolders = []
    files = []
    ext = [".flac", ".mp3"]

    for f in os.scandir(__dir):
        if f.is_dir() and not f.name.startswith("."):
            subfolders.append(f.path)
        if f.is_file():
            if os.path.splitext(f.name)[1].lower() in ext:
                files.append(f.path)

    if full or len(files) == 0:
        for _dir in list(subfolders):
            sf, f = run_fast_scandir(_dir, full=True)
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


def create_album_hash(title: str, artist: str) -> str:
    """
    Creates a simple hash for an album
    """
    return (title + artist).replace(" ", "").lower()


def create_new_date():
    now = datetime.now()
    str = now.strftime("%Y-%m-%d %H:%M:%S")
    return str


def create_safe_name(name: str) -> str:
    """
    Creates a url-safe name from a name.
    """
    return "".join([i for i in name if i not in '/\\:*?"<>|'])


class UseBisection:

    def __init__(self, list: List, search_from: str,
                 queries: List[str]) -> None:
        self.list = list
        self.queries = queries
        self.search_from = search_from
        self.list.sort(key=lambda x: getattr(x, search_from))

    def find(self, query: str):
        left = 0
        right = len(self.list) - 1

        while left <= right:
            mid = (left + right) // 2

            if self.list[mid].__getattribute__(self.search_from) == query:
                return self.list[mid]
            elif self.list[mid].__getattribute__(self.search_from) > query:
                right = mid - 1
            else:
                left = mid + 1

        return None

    def __call__(self) -> Any:
        return [self.find(query) for query in self.queries]
