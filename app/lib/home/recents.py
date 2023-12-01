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


def timestamp_from_days_ago(days_ago):
    current_datetime = datetime.now()
    delta = timedelta(days=days_ago)
    past_timestamp = current_datetime - delta

    past_timestamp = int(past_timestamp.timestamp())

    return past_timestamp


group_type = tuple[str, list[Track]]


def calc_based_on_percent(items: list[str], total: int):
    """
    Checks if items is more than 85% of total items. Returns a boolean and the most common item.
    """
    most_common = max(items, key=items.count)
    most_common_count = items.count(most_common)

    return most_common_count / total >= 0.85, most_common


def check_is_album_folder(group: group_type):
    key, group_ = group
    albumhashes = [t.albumhash for t in group_]
    return calc_based_on_percent(albumhashes, len(group_))


def check_is_artist_folder(group: group_type):
    key, group_ = group
    artisthashes = "-".join(t.artist_hashes for t in group_).split("-")
    return calc_based_on_percent(artisthashes, len(group_))


def check_is_track_folder(group: group_type):
    key, group_ = group

    # is more of a playlist
    if len(group_) >= 3:
        return False

    return [
        {
            "type": "track",
            "item": serialize_track(t, to_remove={"created_date"}),
        }
        for t in group_
    ]


def check_folder_type(group_: group_type) -> str:
    # check if all tracks in group have the same albumhash
    # if so, return "album"
    key, tracks = group_

    if len(tracks) == 1:
        return {
            "type": "track",
            "item": serialize_track(tracks[0], to_remove={"created_date"}),
        }

    is_album, albumhash = check_is_album_folder(group_)
    if is_album:
        album = AlbumStore.get_album_by_hash(albumhash)
        return {
            "type": "album",
            "item": album_serializer(
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
            ),
        }

    is_artist, artisthash = check_is_artist_folder(group_)
    if is_artist:
        artist = ArtistStore.get_artist_by_hash(artisthash)
        artist = serialize_for_card(artist)
        artist["trackcount"] = len(tracks)

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
            },
        }
    )


def group_track_by_folders(tracks: Track) -> (str, list[Track]):
    tracks = sorted(tracks, key=lambda t: t.folder)
    groups = groupby(tracks, lambda t: t.folder)
    groups = ((k, list(g)) for k, g in groups)

    # sort groups by last modified date
    return sorted(groups, key=lambda g: os.path.getctime(g[0]), reverse=True)


def get_recent_items(cutoff_days: int):
    timestamp = timestamp_from_days_ago(cutoff_days)

    tracks = (t for t in TrackStore.tracks if t.created_date > timestamp)
    tracks = sorted(tracks, key=lambda t: t.created_date)

    groups = group_track_by_folders(tracks)

    recent_items = []

    for group in groups:
        item = check_folder_type(group)

        if item not in recent_items:
            recent_items.append(item) if type(item) == dict else recent_items.extend(
                item
            )

    return recent_items
