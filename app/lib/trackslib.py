"""
This library contains all the functions related to tracks.
"""
import os

from app.lib.pydub.pydub import AudioSegment
from app.lib.pydub.pydub.silence import detect_leading_silence, detect_silence

from app.db.sqlite.tracks import SQLiteTrackMethods as tdb
from app.store.tracks import TrackStore
from app.utils.progressbar import tqdm
from app.utils.threading import ThreadWithReturnValue


def validate_tracks() -> None:
    """
    Removes track records whose files no longer exist.
    """
    for track in tqdm(TrackStore.tracks, desc="Validating tracks"):
        if not os.path.exists(track.filepath):
            TrackStore.remove_track_obj(track)
            tdb.remove_tracks_by_filepaths(track.filepath)


def get_leading_silence_end(filepath: str):
    """
    Returns the leading silence of a track.
    """
    format = filepath.split(".")[-1]
    audio = AudioSegment.from_file(filepath, format=format)
    silence = detect_leading_silence(audio, silence_threshold=-40.0, chunk_size=10)

    return silence if silence > 1000 else 0


def get_trailing_silence_start(filepath: str):
    """
    Returns the trailing silence of a track.
    """
    format = filepath.split(".")[-1]
    audio = AudioSegment.from_file(filepath, format=format)
    duration = len(audio)

    audio = audio[-30000:] if len(audio) > 30000 else audio
    silence_groups = detect_silence(audio, silence_thresh=-40.0, seek_step=10)

    if len(silence_groups) == 0:
        return duration

    silence_group = silence_groups[-1]
    is_ok = silence_group[1] == len(audio)

    if is_ok:
        return duration - (silence_group[1] - silence_group[0])

    return duration


def get_silence_paddings(ending_file: str, starting_file: str):
    """
    Returns the ending silence of a track and the starting silence of the next.
    """
    silence = {"start": 0, "end": 0}
    ending_thread = None
    starting_thread = None

    if os.path.exists(ending_file):
        ending_thread = ThreadWithReturnValue(
            target=get_trailing_silence_start, args=(ending_file,)
        )
        ending_thread.start()

    if os.path.exists(starting_file):
        starting_thread = ThreadWithReturnValue(
            target=get_leading_silence_end, args=(starting_file,)
        )
        starting_thread.start()

    if ending_thread:
        silence["end"] = ending_thread.join()

    if starting_thread:
        silence["start"] = starting_thread.join()

    return silence
