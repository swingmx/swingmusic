from itertools import groupby
import os
from pprint import pprint
from app.lib.albumslib import sort_by_track_no
from app.models.folder import Folder
from app.models.track import Track
from app.utils import flatten


def sort_tracks(tracks: list[Track], key: str, reverse: bool = False):
    """
    Sorts a list of tracks by a key.
    """
    if key == "default":
        return tracks

    sortfunc = lambda x: getattr(x, key)

    if key == "artists" or key == "albumartists":
        sortfunc = lambda x: getattr(x, key)[0]["name"]

    if key == "disc":
        # INFO: Group tracks into albums, then sort them by disc number.
        tracks = sorted(tracks, key=lambda x: x.album)
        groups = groupby(tracks, lambda x: x.albumhash)

        return flatten([sort_by_track_no(list(g)) for k, g in groups])

    # INFO: sort tracks by title for a fallback value
    tracks = sorted(tracks, key=lambda t: t.title)

    if key == "title" and not reverse:
        return tracks

    return sorted(tracks, key=sortfunc, reverse=reverse)


def sort_folders(folders: list[Folder], key: str, reverse: bool = False):
    """
    Sorts a list of folders by a key.
    """
    if key == "default":
        return folders

    sortfunc = lambda x: getattr(x, key)

    if key == "lastmod":
        sortfunc = lambda x: os.path.getmtime(x.path)

    return sorted(folders, key=sortfunc, reverse=reverse)
