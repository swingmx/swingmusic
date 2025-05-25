"""
Contains methods relating to albums.
"""


from swingmusic.models.track import Track


def remove_duplicate_on_merge_versions(tracks: list[Track]):
    """
    Removes duplicate tracks when merging versions of the same album.
    """
    # TODO!
    pass


def sort_by_track_no(tracks: list[Track]):
    for t in tracks:
        track = str(t.track).zfill(3)
        t._pos = int(f"{t.disc}{track}")

    tracks = sorted(tracks, key=lambda t: t._pos)

    return tracks
