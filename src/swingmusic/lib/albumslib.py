"""
Contains methods relating to albums.
"""

from swingmusic.models.album import Album
from swingmusic.models.track import Track
from swingmusic.store.tracks import TrackStore
from swingmusic.utils.parsers import get_base_album_title
from swingmusic.utils.remove_duplicates import remove_duplicates


def remove_duplicate_on_merge_versions(tracks: list[Track]):
    """
    Removes duplicate tracks when merging versions of the same album.
    """
    # TODO!
    pass


def sort_by_track_no(tracks: list[Track]) -> list[Track]:
    """
    Sort tracks by track number.
    Track numbers cannot be longer than three positions.

    :param tracks: List of Tracks
    :return: Sorted list of Tracks
    """
    for t in tracks:
        track = str(t.track).zfill(3)
        t._pos = int(f"{t.disc}{track}")

    tracks = sorted(tracks, key=lambda t: t._pos)

    return tracks


def create_albums(_trackhashes: list[str] = []) -> list[tuple[Album, set[str]]]:
    """
    Creates album objects using the indexed tracks. Takes in an optional
    list of trackhashes to create the albums from. If no list is provided,
    all tracks are used.

    The trackhashes are passed when creating albums from the watchdogg module.

    Returns a list of tuples containing the album and the trackhashes in the album.
    ie:

    >>> list[tuple[Album, set[str]]]
    """
    albums = dict()

    if _trackhashes:
        all_tracks: list[Track] = TrackStore.get_tracks_by_trackhashes(_trackhashes)
    else:
        all_tracks: list[Track] = TrackStore.get_flat_list()

    all_tracks = remove_duplicates(all_tracks)

    for track in all_tracks:
        if track.albumhash not in albums:
            albums[track.albumhash] = {
                "albumartists": track.albumartists,
                "artisthashes": [a["artisthash"] for a in track.albumartists],
                "albumhash": track.albumhash,
                "base_title": None,
                "color": None,
                "created_date": track.last_mod,
                "date": track.date,
                "duration": track.duration,
                "genres": [*track.genres] if track.genres else [],
                "og_title": track.og_album,
                "lastplayed": track.lastplayed,
                "playcount": track.playcount,
                "playduration": track.playduration,
                "title": track.album,
                "tracks": {track.trackhash},
                "pathhash": track.pathhash,
                "extra": {},
            }
        else:
            album = albums[track.albumhash]
            album["tracks"].add(track.trackhash)
            album["playcount"] += track.playcount
            album["playduration"] += track.playduration
            album["lastplayed"] = max(album["lastplayed"], track.lastplayed)
            album["duration"] += track.duration
            album["date"] = min(album["date"], track.date)
            album["created_date"] = min(album["created_date"], track.last_mod)

            if track.genres:
                album["genres"].extend(track.genres)

    for album in albums.values():
        genres = []
        for genre in album["genres"]:
            if genre not in genres:
                genres.append(genre)

        album["genres"] = genres
        album["genrehashes"] = " ".join([g["genrehash"] for g in genres])
        album["base_title"], _ = get_base_album_title(album["og_title"])
        album["blurhash"] = ""

        del genres
        trackhashes = album.pop("tracks")
        album["trackcount"] = len(trackhashes)

        albums[album["albumhash"]] = (Album(**album), trackhashes)

    return list(albums.values())
