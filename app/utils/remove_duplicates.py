from collections import defaultdict
from operator import attrgetter

from app.models import Track
from app.utils.hashing import create_hash


def remove_duplicates(tracks: list[Track], is_album_tracks=False) -> list[Track]:
    """
    Remove duplicates from a list of Track objects based on the trackhash attribute.

    Retain objects with the highest bitrate.
    """
    tracks_dict = defaultdict(list)

    # if is_album_tracks, sort by disc and track number
    if is_album_tracks:
        for t in tracks:
            # _pos is used for sorting tracks by disc and track number
            t._pos = int(f"{t.disc}{str(t.track).zfill(3)}")

            # _ati is used to remove duplicates when merging album versions
            t._ati = f"{t._pos}{create_hash(t.title)}"

        # create groups of tracks with the same _ati
        for track in tracks:
            tracks_dict[track._ati].append(track)

        tracks = []

        # pick the track with max bitrate for each group
        for track_group in tracks_dict.values():
            max_bitrate_track = max(track_group, key=attrgetter("bitrate"))
            tracks.append(max_bitrate_track)

        return sorted(tracks, key=lambda t: t._pos)

    # else, sort by trackhash
    for track in tracks:
        # create groups of tracks with the same trackhash
        tracks_dict[track.trackhash].append(track)

    tracks = []

    # pick the track with max bitrate for each trackhash group
    for track_group in tracks_dict.values():
        max_bitrate_track = max(track_group, key=attrgetter("bitrate"))
        tracks.append(max_bitrate_track)

    return tracks
