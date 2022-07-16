"""
This module contains mini functions for the server.
"""
import os
from pprint import pprint
import threading
from datetime import datetime
from typing import Dict, List, Set

import requests

from app import instances, models


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


class RemoveDuplicates:
    def __init__(self, tracklist: List[models.Track]) -> None:
        self.tracklist = tracklist

    def __call__(self) -> List[models.Track]:
        uniq_hashes = []
        [
            uniq_hashes.append(t.uniq_hash)
            for t in self.tracklist
            if t.uniq_hash not in uniq_hashes
        ]
        tracks = UseBisection(self.tracklist, "uniq_hash", uniq_hashes)()

        return tracks


def is_valid_file(filename: str) -> bool:
    """
    Checks if a file is valid. Returns True if it is, False if it isn't.
    """

    if filename.endswith(".flac") or filename.endswith(".mp3"):
        return True
    else:
        return False


def create_hash(*args: List[str]) -> str:
    """
    Creates a simple hash for an album
    """
    string = "".join(a for a in args).replace(" ", "")
    return "".join([i for i in string if i.isalnum()]).lower()


def create_new_date():
    now = datetime.now()
    str = now.strftime("%Y-%m-%d %H:%M:%S")
    return str


def create_safe_name(name: str) -> str:
    """
    Creates a url-safe name from a name.
    """
    return "".join([i for i in name if i.isalnum()]).lower()


class UseBisection:
    """
    Uses bisection to find a list of items in another list.

    returns a list of found items with `None` items being not found
    items.
    """

    def __init__(self, source: List, search_from: str, queries: List[str]) -> None:
        self.source_list = source
        self.queries_list = queries
        self.attr = search_from
        self.source_list.sort(key=lambda x: getattr(x, search_from))

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

    def __call__(self) -> List:
        if len(self.source_list) == 0:
            print("🚀🚀🚀🚀🚀🚀🚀")
            return [None]

        return [self.find(query) for query in self.queries_list]


class Get:
    @staticmethod
    def get_all_tracks() -> List[models.Track]:
        """
        Returns all tracks
        """
        t = instances.tracks_instance.get_all_tracks()
        return [models.Track(t) for t in t]

    def get_all_albums() -> List[models.Album]:
        """
        Returns all albums
        """
        a = instances.album_instance.get_all_albums()
        return [models.Album(a) for a in a]

    @classmethod
    def get_all_artists(cls) -> Set[str]:
        tracks = cls.get_all_tracks()
        artists: Set[str] = set()

        for track in tracks:
            for artist in track.artists:
                artists.add(artist)

        return artists

    @staticmethod
    def get_all_playlists() -> List[models.Playlist]:
        """
        Returns all playlists
        """
        p = instances.playlist_instance.get_all_playlists()
        return [models.Playlist(p) for p in p]


class Ping:
    """Checks if there is a connection to the internet by pinging google.com"""

    @staticmethod
    def __call__() -> bool:
        try:
            requests.get("https://google.com", timeout=10)
            return True
        except (requests.exceptions.ConnectionError, requests.Timeout):
            return False


def get_normal_artist_name(artists: List[str]) -> str:
    """
    Returns the artist name with most capital letters.
    """
    if len(artists) == 1:
        return artists[0]

    artists.sort()
    return artists[0]


def get_artist_lists(artists: List[str]) -> List[str]:
    """
    Takes in a list of artists and returns a list of lists of an artist's various name variations.

    Example:
    >>> get_artist_lists(['Juice WRLD', 'Juice Wrld', 'XXXtentacion', 'XXXTENTACION'])

    >>> [['Juice WRLD', 'Juice Wrld'], ['XXXtentacion', 'XXXTENTACION']]
    """
    artist_lists: List[List[str]] = []

    for artist in artists:
        for list in artist_lists:
            if artist.lower() == list[0].lower():
                list.append(artist)
                break
        else:
            artist_lists.append([artist])

    return artist_lists


def get_normalized_artists(names: List[str]) -> List[models.Artist]:
    """
    Takes in a list of artists and returns a list of models.Artist objects with normalized names.
    """
    names = [n.strip() for n in names]
    names = get_artist_lists(names)
    names = [get_normal_artist_name(a) for a in names]

    return [models.Artist(a) for a in names]
