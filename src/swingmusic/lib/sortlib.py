from itertools import groupby
import os
from typing import Callable
from swingmusic.lib.albumslib import sort_by_track_no
from swingmusic.models.folder import Folder
from swingmusic.models.track import Track
from swingmusic.utils import flatten


def sort_tracks(tracks: list[Track], key: str, reverse: bool = False):
    """
    Sorts a list of tracks by a key.
    """
    if key == "default":
        return tracks

    sortfunc: Callable[[Track], str] = lambda track: getattr(track, key)
    if key == "artists" or key == "albumartists":
        sortfunc = lambda track: getattr(track, key)[0]["name"]

    if key == "disc":
        # INFO: Group tracks into albums, then sort them by disc number.
        tracks = sorted(tracks, key=lambda x: x.album.casefold())
        groups = groupby(tracks, lambda x: x.albumhash)

        return flatten([sort_by_track_no(list(g)) for k, g in groups])

    # INFO: sort tracks by title for a fallback value
    tracks = sorted(tracks, key=lambda t: t.title.casefold())

    if key == "title" and not reverse:
        return tracks

    return sorted(
        tracks,
        key=lambda track: sortfunc(track).casefold()
        if isinstance(sortfunc(track), str)
        else sortfunc(track),
        reverse=reverse,
    )


def sort_folders(folders: list[Folder], key: str, reverse: bool = False):
    """
    Sorts a list of folders by a key.
    """
    if key == "default":
        return folders

    sortfunc: Callable[[Folder], str | float] = lambda folder: getattr(folder, key)

    if key == "lastmod":
        sortfunc = lambda folder: os.path.getmtime(folder.path)

    return sorted(folders, key=sortfunc, reverse=reverse)
