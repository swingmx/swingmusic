"""
This library contains all the functions related to tracks.
"""
import os

from tqdm import tqdm

from app.db.sqlite.tracks import SQLiteTrackMethods as tdb
from app.store.tracks import TrackStore


def validate_tracks() -> None:
    """
    Gets all songs under the ~/ directory.
    """
    for track in tqdm(TrackStore.tracks, desc="Removing deleted tracks"):
        if not os.path.exists(track.filepath):
            print(f"Removing {track.filepath}")
            TrackStore.tracks.remove(track)
            tdb.remove_track_by_filepath(track.filepath)
