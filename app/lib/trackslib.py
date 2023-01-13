"""
This library contains all the functions related to tracks.
"""
import os

from tqdm import tqdm

from app.db.store import Store
from app.db.sqlite.tracks import SQLiteTrackMethods as tdb


def validate_tracks() -> None:
    """
    Gets all songs under the ~/ directory.
    """
    for track in tqdm(Store.tracks, desc="Removing deleted tracks"):
        if not os.path.exists(track.filepath):
            Store.tracks.remove(track)
            tdb.remove_track_by_filepath(track.filepath)
