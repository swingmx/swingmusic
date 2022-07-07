"""
This library contains all the functions related to tracks.
"""
import os

from app import instances
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


def get_p_track(ptrack):
    return instances.tracks_instance.find_track_by_title_artists_album(
        ptrack["title"], ptrack["artists"], ptrack["album"])
