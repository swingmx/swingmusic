"""
This library contains all the functions related to tracks.
"""
import os
from typing import List

from app import api, instances, models
from app.helpers import remove_duplicates
from app.lib import albumslib
from progress.bar import Bar


def create_all_tracks() -> List[models.Track]:
    """
    Gets all songs under the ~/ directory.
    """
    tracks: list[models.Track] = []

    _bar = Bar("Creating tracks", max=len(api.DB_TRACKS))

    for track in api.DB_TRACKS:
        try:
            os.chmod(track["filepath"], 0o755)
        except FileNotFoundError:
            instances.tracks_instance.remove_song_by_id(track["_id"]["$oid"])
            api.DB_TRACKS.remove(track)

        tracks.append(models.Track(track))
        _bar.next()

    _bar.finish()

    return tracks


def get_album_tracks(albumname, artist):
    """Returns api tracks matching an album"""
    _tracks: List[models.Track] = []

    for track in api.TRACKS:
        if track.album == albumname and track.albumartist == artist:
            _tracks.append(track)

    return remove_duplicates(_tracks)


def get_track_by_id(trackid: str) -> models.Track:
    """Returns api track matching an id"""
    for track in api.TRACKS:
        if track.trackid == trackid:
            return track
