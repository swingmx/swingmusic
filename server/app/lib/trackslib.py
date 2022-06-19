"""
This library contains all the functions related to tracks.
"""
import os
from pprint import pprint
from typing import List

from app import api, instances, models
from app.helpers import remove_duplicates
from tqdm import tqdm


def validate_tracks() -> None:
    """
    Gets all songs under the ~/ directory.
    """
    entries = instances.tracks_instance.get_all_tracks()

    for track in tqdm(entries, desc="Validating tracks"):
        try:
            os.chmod(track["filepath"], 0o755)
        except FileNotFoundError:
            instances.tracks_instance.remove_song_by_id(track["_id"]["$oid"])


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
        try:
            if track.trackid == trackid:
                return track
        except AttributeError:
            print("AttributeError")


def find_track(tracks: list, hash: str) -> int | None:
    """
    Finds an album by album title and artist.
    """

    left = 0
    right = len(tracks) - 1
    iter = 0

    while left <= right:
        iter += 1
        mid = (left + right) // 2

        if tracks[mid]["albumhash"] == hash:
            return mid

        if tracks[mid]["albumhash"] < hash:
            left = mid + 1
        else:
            right = mid - 1

    return None


def get_p_track(ptrack):
    return instances.tracks_instance.find_track_by_title_artists_album(
        ptrack["title"], ptrack["artists"], ptrack["album"]
    )
