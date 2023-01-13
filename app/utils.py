"""
This module contains mini functions for the server.
"""
import os
import hashlib
from pathlib import Path
import threading
from datetime import datetime
from unidecode import unidecode
import requests

from app import models
from app.settings import SUPPORTED_FILES

CWD = Path(__file__).parent.resolve()


def background(func):
    """
    a threading decorator
    use @background above the function you want to run in the background
    """

    def background_func(*a, **kw):
        threading.Thread(target=func, args=a, kwargs=kw).start()

    return background_func


def run_fast_scandir(__dir: str, full=False) -> tuple[list[str], list[str]]:
    """
    Scans a directory for files with a specific extension. Returns a list of files and folders in the directory.
    """

    subfolders = []
    files = []

    for f in os.scandir(__dir):
        if f.is_dir() and not f.name.startswith("."):
            subfolders.append(f.path)
        if f.is_file():
            ext = os.path.splitext(f.name)[1].lower()
            if ext in SUPPORTED_FILES:
                files.append(f.path)

    if full or len(files) == 0:
        for _dir in list(subfolders):
            sf, f = run_fast_scandir(_dir, full=True)
            subfolders.extend(sf)
            files.extend(f)

    return subfolders, files


def remove_duplicates(tracks: list[models.Track]) -> list[models.Track]:
    """
    Removes duplicate tracks from a list of tracks.
    """
    hashes = []

    for track in tracks:
        if track.trackhash not in hashes:
            hashes.append(track.trackhash)

    tracks = sorted(tracks, key=lambda x: x.trackhash)
    tracks = UseBisection(tracks, "trackhash", hashes)()

    return [t for t in tracks if t is not None]


def create_hash(*args: str, decode=False, limit=7) -> str:
    """
    Creates a simple hash for an album
    """
    string = "".join(args)

    if decode:
        string = unidecode(string)

    string = string.lower().strip().replace(" ", "")
    string = "".join(t for t in string if t.isalnum())
    string = string.encode("utf-8")
    string = hashlib.sha256(string).hexdigest()
    return string[-limit:]


def create_folder_hash(*args: str, limit=7) -> str:
    """
    Creates a simple hash for an album
    """
    strings = [s.lower().strip().replace(" ", "") for s in args]

    strings = ["".join([t for t in s if t.isalnum()]) for s in strings]
    strings = [s.encode("utf-8") for s in strings]
    strings = [hashlib.sha256(s).hexdigest()[-limit:] for s in strings]
    return "".join(strings)


def create_new_date():
    """
    It creates a new date and time string in the format of "YYYY-MM-DD HH:MM:SS"
    :return: A string of the current date and time.
    """
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


class UseBisection:
    """
    Uses bisection to find a list of items in another list.

    returns a list of found items with `None` items being not found
    items.
    """

    def __init__(self, source: list, search_from: str, queries: list[str]) -> None:
        self.source_list = source
        self.queries_list = queries
        self.attr = search_from

    def find(self, query: str):
        left = 0
        right = len(self.source_list) - 1

        while left <= right:
            mid = (left + right) // 2
            if self.source_list[mid].__getattribute__(self.attr) == query:
                return self.source_list[mid]
            elif self.source_list[mid].__getattribute__(self.attr) > query:
                right = mid - 1
            else:
                left = mid + 1

        return None

    def __call__(self) -> list:
        if len(self.source_list) == 0:
            return [None]

        return [self.find(query) for query in self.queries_list]


class Ping:
    """
    Checks if there is a connection to the internet by pinging google.com
    """

    @staticmethod
    def __call__() -> bool:
        try:
            requests.get("https://google.com", timeout=10)
            return True
        except (requests.exceptions.ConnectionError, requests.Timeout):
            return False


def get_artists_from_tracks(tracks: list[models.Track]) -> set[str]:
    """
    Extracts all artists from a list of tracks. Returns a list of Artists.
    """
    artists = set()

    master_artist_list = [[x.name for x in t.artist] for t in tracks]  # type: ignore
    artists = artists.union(*master_artist_list)

    return artists


def get_albumartists(albums: list[models.Album]) -> set[str]:
    artists = set()

    # master_artist_list = [a.albumartists for a in albums]
    for album in albums:
        albumartists = [a.name for a in album.albumartists]  # type: ignore

        artists.update(albumartists)

    # return [models.Artist(a) for a in artists]
    return artists


def get_all_artists(
    tracks: list[models.Track], albums: list[models.Album]
) -> list[models.Artist]:
    artists_from_tracks = get_artists_from_tracks(tracks)
    artist_from_albums = get_albumartists(albums)

    artists = list(artists_from_tracks.union(artist_from_albums))
    artists = sorted(artists)

    lower_artists = set(a.lower().strip() for a in artists)
    indices = [[ar.lower().strip() for ar in artists].index(a) for a in lower_artists]
    artists = [artists[i] for i in indices]

    return [models.Artist(a) for a in artists]


def bisection_search_string(strings: list[str], target: str) -> str | None:
    """
    Finds a string in a list of strings using bisection search.
    """
    if not strings:
        return None

    strings = sorted(strings)

    left = 0
    right = len(strings) - 1
    while left <= right:
        middle = (left + right) // 2
        if strings[middle] == target:
            return strings[middle]

        if strings[middle] < target:
            left = middle + 1
        else:
            right = middle - 1

    return None


def get_home_res_path(filename: str):
    """
    Returns a path to resources in the home directory of this project. Used to resolve resources in builds.
    """
    return (CWD / ".." / filename).resolve()
