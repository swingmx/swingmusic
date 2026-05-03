import json
from typing import Any
from swingmusic.db.userdata import PlaylistTable
from swingmusic.lib.playlistlib import get_first_4_images
from swingmusic.serializers.album import serialize_for_card
from swingmusic.serializers.artist import serialize_for_card as serialize_artist
from swingmusic.serializers.playlist import serialize_for_card as serialize_playlist
from swingmusic.serializers.track import serialize_track
from swingmusic.store.albums import AlbumStore
from swingmusic.store.artists import ArtistStore
from swingmusic.store.tracks import TrackStore
from swingmusic.utils.hashing import create_hash


def validate_page_items(items: list[dict[str, str]], existing: list[dict[str, str]]):
    """
    Validate the items in a page before adding them to the database.
    """
    validated: list[dict[str, str]] = []
    indexed = set(create_hash(json.dumps(item)) for item in existing)

    for item in items:
        if create_hash(json.dumps(item)) in indexed:
            continue

        item_type = item.get("type")
        item_hash = item.get("hash")

        if item_type is None or item_hash is None:
            raise ValueError("Invalid item payload: missing 'type' or 'hash'")

        if item_type == "album":
            album = AlbumStore.get_album_by_hash(item_hash)

            if album is not None:
                validated.append(item)
        elif item_type == "artist":
            artist = ArtistStore.get_artist_by_hash(item_hash)

            if artist is not None:
                validated.append(item)
        elif item_type == "playlist":
            try:
                playlist_id = int(item_hash)
            except (TypeError, ValueError):
                playlist_id = -1

            playlist = PlaylistTable.get_by_id(playlist_id)
            if playlist is not None:
                # Normalize hash for stable dedupe/remove behavior.
                normalized_item = dict(item)
                normalized_item["hash"] = str(playlist_id)
                validated.append(normalized_item)
        elif item_type == "track":
            track = TrackStore.trackhashmap.get(item_hash)
            if track is not None:
                validated.append(item)
        else:
            raise ValueError(f"Invalid item type: {item_type}")

    return validated


def remove_page_items(existing: list[dict[str, str]], item: dict[str, str]):
    return [
        i
        for i in existing
        if create_hash(json.dumps(i)) != create_hash(json.dumps(item))
    ]


def recover_page_items(items: list[dict[str, str]], for_homepage: bool = False):
    """
    Recover the items in a page.
    """
    recovered: list[dict[str, Any]] = []

    for item in items:
        item_type = item.get("type")
        item_hash = item.get("hash")

        if item_type is None or item_hash is None:
            continue

        if item_type == "album":
            album = AlbumStore.get_album_by_hash(item_hash)

            if album is not None:
                item = serialize_for_card(album)
                item["type"] = "album"

                if for_homepage:
                    item.pop("type", None)
                    item = {"item": item, "type": "album"}

                recovered.append(item)
        elif item_type == "artist":
            artist = ArtistStore.get_artist_by_hash(item_hash)

            if artist is not None:
                item = serialize_artist(artist)
                item["type"] = "artist"

                if for_homepage:
                    item.pop("type", None)
                    item = {"item": item, "type": "artist"}

                recovered.append(item)
        elif item_type == "playlist":
            try:
                playlist_id = int(item_hash)
            except (TypeError, ValueError):
                continue

            playlist = PlaylistTable.get_by_id(playlist_id)
            if playlist is not None:
                if not playlist.has_image:
                    tracks = TrackStore.get_tracks_by_trackhashes(playlist.trackhashes)
                    playlist.images = get_first_4_images(tracks)

                playlist.clear_lists()
                item = serialize_playlist(playlist)
                item["type"] = "playlist"

                if for_homepage:
                    item.pop("type", None)
                    item = {"item": item, "type": "playlist"}

                recovered.append(item)
        elif item_type == "track":
            track_group = TrackStore.trackhashmap.get(item_hash)
            if track_group is not None:
                item = serialize_track(track_group.get_best())
                item["type"] = "track"

                if for_homepage:
                    item.pop("type", None)
                    item = {"item": item, "type": "track"}

                recovered.append(item)

    recovered.reverse()
    return recovered
