"""
This library contains all the functions related to tracks.
"""
import os


from app.db.sqlite.tracks import SQLiteTrackMethods as tdb
from app.store.tracks import TrackStore
from app.utils.progressbar import tqdm

def validate_tracks() -> None:
    """
    Removes track records whose files no longer exist.
    """
    for track in tqdm(TrackStore.tracks, desc="Validating tracks"):
        if not os.path.exists(track.filepath):
            TrackStore.remove_track_obj(track)
            tdb.remove_tracks_by_filepaths(track.filepath)
