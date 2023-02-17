"""
This module contains mini functions for the server.
"""
import hashlib
import os
import platform
import random
import re
import socket as Socket
import string
import threading
from datetime import datetime
from pathlib import Path

import requests
from unidecode import unidecode

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


def run_fast_scandir(_dir: str, full=False) -> tuple[list[str], list[str]]:
    """
    Scans a directory for files with a specific extension.
    Returns a list of files and folders in the directory.
    """

    if _dir == "":
        return [], []

    subfolders = []
    files = []

    try:
        for _file in os.scandir(_dir):
            if _file.is_dir() and not _file.name.startswith("."):
                subfolders.append(_file.path)
            if _file.is_file():
                ext = os.path.splitext(_file.name)[1].lower()
                if ext in SUPPORTED_FILES:
                    files.append(win_replace_slash(_file.path))

        if full or len(files) == 0:
            for _dir in list(subfolders):
                sub_dirs, _file = run_fast_scandir(_dir, full=True)
                subfolders.extend(sub_dirs)
                files.extend(_file)
    except (OSError, PermissionError, FileNotFoundError, ValueError):
        return [], []

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

    for album in albums:
        albumartists = [a.name for a in album.albumartists]  # type: ignore

        artists.update(albumartists)

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
    Returns a path to resources in the home directory of this project.
    Used to resolve resources in builds.
    """
    try:
        return (CWD / ".." / filename).resolve()
    except ValueError:
        return None


def get_ip():
    """
    Returns the IP address of this device.
    """
    soc = Socket.socket(Socket.AF_INET, Socket.SOCK_DGRAM)
    soc.connect(("8.8.8.8", 80))
    ip_address = str(soc.getsockname()[0])
    soc.close()

    return ip_address


def is_windows():
    """
    Returns True if the OS is Windows.
    """
    return platform.system() == "Windows"


def parse_feat_from_title(title: str) -> tuple[list[str], str]:
    """
    Extracts featured artists from a song title using regex.
    """
    regex = r"\((?:feat|ft|featuring|with)\.?\s+(.+?)\)"
    # regex for square brackets 👇
    sqr_regex = r"\[(?:feat|ft|featuring|with)\.?\s+(.+?)\]"

    match = re.search(regex, title, re.IGNORECASE)

    if not match:
        match = re.search(sqr_regex, title, re.IGNORECASE)
        regex = sqr_regex

    if not match:
        return [], title

    artists = match.group(1)
    artists = split_artists(artists, with_and=True)

    # remove "feat" group from title
    new_title = re.sub(regex, "", title, flags=re.IGNORECASE)
    return artists, new_title


def get_random_str(length=5):
    """
    Generates a random string of length `length`.
    """
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def win_replace_slash(path: str):
    if is_windows():
        return path.replace("\\", "/").replace("//", "/")

    return path


def split_artists(src: str, with_and: bool = False):
    exp = r"\s*(?:and|&|,|;)\s*" if with_and else r"\s*[,;]\s*"

    artists = re.split(exp, src)
    return [a.strip() for a in artists]


def parse_artist_from_filename(title: str):
    """
    Extracts artist names from a song title using regex.
    """

    regex = r"^(.+?)\s*[-–—]\s*(?:.+?)$"
    match = re.search(regex, title, re.IGNORECASE)

    if not match:
        return []

    artists = match.group(1)
    artists = split_artists(artists)
    return artists


def parse_title_from_filename(title: str):
    """
    Extracts track title from a song title using regex.
    """

    regex = r"^(?:.+?)\s*[-–—]\s*(.+?)$"
    match = re.search(regex, title, re.IGNORECASE)

    if not match:
        return title

    res = match.group(1)
    # remove text in brackets starting with "official" case-insensitive
    res = re.sub(r"\s*\([^)]*official[^)]*\)", "", res, flags=re.IGNORECASE)
    return res.strip()


def remove_prod(title: str) -> str:
    """
    Removes the producer string in a track title using regex.
    """

    # check if title contain title, if not return it.
    if not ("prod." in title.lower()):
        return title

    # check if title has brackets
    if re.search(r'[()\[\]]', title):
        regex = r'\s?(\(|\[)prod\..*?(\)|\])\s?'
    else:
        regex = r'\s?\bprod\.\s*\S+'

    # remove the producer string
    title = re.sub(regex, "", title, flags=re.IGNORECASE)
    return title.strip()
