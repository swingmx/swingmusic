import os
from natsort import natsorted
from itertools import groupby
from swingmusic.utils import flatten
from swingmusic.models.track import Track
from swingmusic.models.folder import Folder
from swingmusic.lib.albumslib import sort_by_track_no


def sort_tracks(tracks: list[Track], key: str, reverse: bool = False):
    """
    Sorts a list of tracks by a key.
    """

    # INFO: This is the primary sortfunc used to get base sort order
    def primary_sortfunc(track: Track) -> str:
        return track.title.casefold()

    if key == "default":
        # INFO: When sorting using default sort, use last_mod as base sort order
        def primary_sortfunc(track: Track) -> float:
            return track.last_mod

    # INFO: This is the secondary sortfunc
    def sortfunc(track: Track) -> str:
        return getattr(track, key)

    if key == "artists" or key == "albumartists":
        # INFO: Sort artists by first artist name
        def sortfunc(track):
            return getattr(track, key)[0]["name"]

    if key == "disc":
        # INFO: Group tracks into albums, then sort them by disc number.
        tracks = natsorted(tracks, key=lambda x: x.album.casefold())
        groups = groupby(tracks, lambda x: x.albumhash)

        return flatten([sort_by_track_no(list(g)) for k, g in groups])

    # INFO: Primary sort: Sort tracks to get base sort order
    tracks = natsorted(tracks, key=primary_sortfunc)

    # INFO: return tracks here if already natsorted (with base sort key)
    if key in ("default", "last_mod", "title"):
        return tracks if not reverse else tracks[::-1]

    # INFO: Final sort and return results
    return natsorted(
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

    def sortfunc(folder: Folder) -> str | float:
        return getattr(folder, key)

    if key == "lastmod":

        def sortfunc(folder):
            return os.path.getmtime(folder.path)

    return natsorted(folders, key=sortfunc, reverse=reverse)
