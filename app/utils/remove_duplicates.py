from collections import defaultdict
from operator import attrgetter

from app.models import Track


def remove_duplicates(tracks: list[Track]) -> list[Track]:
    """
    Remove duplicates from a list of Track objects based on the trackhash attribute.
    Retains objects with the highest bitrate.
    """
    hash_to_tracks = defaultdict(list)

    for track in tracks:
        hash_to_tracks[track.trackhash].append(track)

    tracks = []

    for track_group in hash_to_tracks.values():
        max_bitrate_track = max(track_group, key=attrgetter("bitrate"))
        tracks.append(max_bitrate_track)

    return tracks
