"""
Contains methods relating to albums.
"""

from dataclasses import asdict
from typing import Any


from app.logger import log
from app.models.track import Track
from app.store.albums import AlbumStore
from app.store.tracks import TrackStore


def validate_albums():
    """
    Removes albums that have no tracks.

    Probably albums that were added from incompletely written files.
    """

    album_hashes = {t.albumhash for t in TrackStore.tracks}
    albums = AlbumStore.albums

    for album in albums:
        if album.albumhash not in album_hashes:
            AlbumStore.remove_album(album)


def remove_duplicate_on_merge_versions(tracks: list[Track]) -> list[Track]:
    """
    Removes duplicate tracks when merging versions of the same album.
    """

    pass


def sort_by_track_no(tracks: list[Track]) -> list[dict[str, Any]]:
    tracks = [asdict(t) for t in tracks]

    for t in tracks:
        track = str(t["track"]).zfill(3)
        t["_pos"] = int(f"{t['disc']}{track}")

    tracks = sorted(tracks, key=lambda t: t["_pos"])

    return tracks
