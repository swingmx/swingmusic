import os

from flask import g
from app.models.track import Track
from app.store.tracks import TrackStore
from app.store.albums import AlbumStore
from app.store.artists import ArtistStore

from app.serializers.track import serialize_track
from app.serializers.album import album_serializer
from app.serializers.artist import serialize_for_card

from itertools import groupby
from datetime import datetime, timedelta

older_albums = set()
older_artists = set()

group_type = tuple[str, list[Track]]


def timestamp_from_days_ago(days_ago):
    current_datetime = datetime.now()
    delta = timedelta(days=days_ago)
    past_timestamp = current_datetime - delta

    past_timestamp = int(past_timestamp.timestamp())

    return past_timestamp


def calc_based_on_percent(items: list[str], total: int):
    """
    Checks if items is more than 85% of total items. Returns a boolean and the most common item.
    """
    most_common = max(items, key=items.count)
    most_common_count = items.count(most_common)

    return most_common_count / total >= 0.7, most_common, most_common_count


def check_is_album_folder(group: group_type):
    key, group_ = group
    albumhashes = [t.albumhash for t in group_]
    return calc_based_on_percent(albumhashes, len(group_))


def check_is_artist_folder(group: group_type):
    key, group_ = group
    artisthashes = "-".join(t.artist_hashes for t in group_).split("-")
    return calc_based_on_percent(artisthashes, len(group_))


def check_is_new_artist(artisthash: str):
    if artisthash in older_artists:
        return False

    return True


def check_is_new_album(albumhash: str):
    if albumhash in older_albums:
        return False

    return True


def create_track(t: Track):
    track = serialize_track(t, to_remove={"created_date"})
    track["help_text"] = "NEW TRACK"

    return {
        "type": "track",
        "item": track,
    }


def check_is_track_folder(group: group_type):
    key, group_ = group

    # is more of a playlist
    if len(group_) >= 3:
        return False

    return [create_track(t) for t in group_]


def check_folder_type(group_: group_type) -> str:
    # check if all tracks in group have the same albumhash
    # if so, return "album"
    key, tracks = group_

    if len(tracks) == 1:
        return create_track(tracks[0])

    is_album, albumhash, _ = check_is_album_folder(group_)
    if is_album:
        album = AlbumStore.get_album_by_hash(albumhash)

        if album is None:
            return None

        album = album_serializer(
            album,
            to_remove={
                "genres",
                "og_title",
                "date",
                "duration",
                "count",
                "albumartists_hashes",
                "base_title",
            },
        )
        album["help_text"] = (
            "NEW ALBUM" if check_is_new_album(albumhash) else "NEW TRACKS"
        )

        return {
            "type": "album",
            "item": album,
        }

    is_artist, artisthash, trackcount = check_is_artist_folder(group_)
    if is_artist:
        artist = ArtistStore.get_artist_by_hash(artisthash)

        if artist is None:
            return None

        artist = serialize_for_card(artist)
        artist["trackcount"] = trackcount
        artist["help_text"] = (
            "NEW ARTIST" if check_is_new_artist(artisthash) else "NEW MUSIC"
        )

        return {
            "type": "artist",
            "item": artist,
        }

    is_track_folder = check_is_track_folder(group_)
    return (
        is_track_folder
        if is_track_folder
        else {
            "type": "folder",
            "item": {
                "path": key,
                "count": len(tracks),
                "help_text": "NEW MUSIC",
            },
        }
    )


def group_track_by_folders(tracks: Track) -> (str, list[Track]):
    tracks = sorted(tracks, key=lambda t: t.folder)
    groups = groupby(tracks, lambda t: t.folder)
    groups = ((k, list(g)) for k, g in groups)

    # sort groups by last modified date
    return sorted(groups, key=lambda g: os.path.getctime(g[0]), reverse=True)


def get_recent_items(cutoff_days: int, limit: int = 7):
    timestamp = timestamp_from_days_ago(cutoff_days)
    tracks: list[Track] = []

    for t in TrackStore.tracks:
        if t.created_date > timestamp:
            tracks.append(t)
            continue

        older_albums.add(t.albumhash)
        older_artists.add(t.artist_hashes)

    tracks = sorted(tracks, key=lambda t: t.created_date)
    groups = group_track_by_folders(tracks)

    recent_items = []

    for group in groups[:limit]:
        item = check_folder_type(group)

        if item not in recent_items:
            if not item:
                continue

            recent_items.append(item) if type(item) == dict else recent_items.extend(
                item
            )

    return recent_items[:limit]


def get_recent_tracks(cutoff_days: int):
    tracks = sorted(TrackStore.tracks, key=lambda t: t.created_date, reverse=True)
    timestamp = timestamp_from_days_ago(cutoff_days)

    return [t for t in tracks if t.created_date > timestamp]
