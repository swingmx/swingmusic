from datetime import datetime
import os
from app.db.userdata import FavoritesTable, PlaylistTable, ScrobbleTable

from app.models.logger import TrackLog
from app.models.playlist import Playlist
from app.serializers.track import serialize_track
from app.serializers.album import album_serializer
from app.lib.playlistlib import get_first_4_images
from app.store.folder import FolderStore
from app.utils.dates import (
    create_new_date,
    date_string_to_time_passed,
    timestamp_to_time_passed,
)
from app.serializers.artist import serialize_for_card
from app.serializers.playlist import serialize_for_card as serialize_playlist
from app.lib.home.recentlyadded import get_recently_added_playlist

from app.store.albums import AlbumStore
from app.store.tracks import TrackStore
from app.store.artists import ArtistStore


def get_recently_played(
    limit: int, userid: int | None = None, _entries: list[TrackLog] = []
):
    """
    Get the recently played items for the homepage.

    Pass a list of track log entries to use a subset of the scrobble table.
    """
    # TODO: Paginate this
    items = []
    added = set()

    custom_playlists = [
        {"name": "recentlyadded", "handler": get_recently_added_playlist},
        {"name": "recentlyplayed", "handler": get_recently_played_playlist},
    ]

    def create_items(entries: list[TrackLog]):
        for entry in entries:
            if len(items) >= limit:
                break

            if entry.source in added:
                continue

            added.add(entry.source)

            if entry.type == "album":
                album = AlbumStore.albummap.get(entry.type_src)

                if album is None:
                    continue

                item = {
                    "type": "album",
                    "hash": entry.type_src,
                    "timestamp": entry.timestamp,
                }

                items.append(item)
                continue

            if entry.type == "artist":
                artist = ArtistStore.artistmap.get(entry.type_src)

                if artist is None:
                    continue

                items.append(
                    {
                        "type": "artist",
                        "hash": entry.type_src,
                        "timestamp": entry.timestamp,
                    }
                )

                continue

            if entry.type == "folder":
                folder = entry.type_src

                if not folder:
                    continue

                if not folder.endswith("/"):
                    folder += "/"

                is_home_dir = entry.type_src == "$home"

                if is_home_dir:
                    folder = os.path.expanduser("~")

                item = {
                    "type": "folder",
                    "hash": entry.type_src,
                    "timestamp": entry.timestamp,
                }

                items.append(item)
                continue

            if entry.type == "playlist":
                is_custom = entry.type_src in [i["name"] for i in custom_playlists]

                if is_custom:
                    items.append(
                        {
                            "type": "playlist",
                            "hash": entry.type_src,
                            "timestamp": entry.timestamp,
                            "is_custom": True,
                        }
                    )
                    continue

                playlist = PlaylistTable.get_by_id(entry.type_src)
                if playlist is None:
                    continue

                item = {
                    "type": "playlist",
                    "hash": entry.type_src,
                    "timestamp": entry.timestamp,
                }

                items.append(item)
                continue

            if entry.type == "favorite":
                items.append(
                    {
                        "type": "favorite",
                        "timestamp": entry.timestamp,
                    }
                )
                continue

            t = TrackStore.trackhashmap.get(entry.trackhash)

            if t is None:
                continue

            item = {
                "type": "track",
                "hash": entry.trackhash,
                "timestamp": entry.timestamp,
            }
            items.append(item)

    BATCH_SIZE = 200
    current_index = 0

    if len(_entries):
        entries = _entries
        limit = 1
    else:
        entries = ScrobbleTable.get_all(0, BATCH_SIZE, userid=userid)

    max_iterations = 20
    iterations = 0

    while len(items) < limit and iterations < max_iterations:
        create_items(entries)
        current_index += BATCH_SIZE

        if len(items) < limit:
            entries = ScrobbleTable.get_all(
                start=current_index + 1, limit=BATCH_SIZE, userid=userid
            )
            if not entries:
                break

        iterations += 1

    if iterations == max_iterations:
        print(
            f"Warning: Reached maximum iterations ({max_iterations}) while fetching recently played items"
        )

    return items


def recover_recently_played_items(items: list[dict]):
    custom_playlists = [
        {"name": "recentlyadded", "handler": get_recently_added_playlist},
        {"name": "recentlyplayed", "handler": get_recently_played_playlist},
    ]
    recovered = []

    for item in items:
        recovered_item = None

        if item["type"] == "album":
            album = AlbumStore.get_album_by_hash(item["hash"])
            if album is None:
                continue

            album = album_serializer(
                album,
                to_remove={
                    "genres",
                    "date",
                    "count",
                    "duration",
                    "albumartists_hashes",
                    "og_title",
                },
            )

            recovered_item = {
                "type": "album",
                "item": album,
            }
        elif item["type"] == "artist":
            artist = ArtistStore.get_artist_by_hash(item["hash"])
            if artist is None:
                continue

            recovered_item = {
                "type": "artist",
                "item": serialize_for_card(artist),
            }
        elif item["type"] == "folder":
            count = FolderStore.count_tracks_containing_paths([item["hash"]])

            recovered_item = {
                "type": "folder",
                "item": {
                    "path": item["hash"],
                    "count": count[0]["trackcount"],
                },
            }
        elif item["type"] == "playlist":
            if item["is_custom"]:
                playlist, _ = next(
                    i["handler"]()
                    for i in custom_playlists
                    if i["name"] == item["hash"]
                )
                playlist.images = [i["image"] for i in playlist.images]

                playlist = serialize_playlist(
                    playlist, to_remove={"settings", "duration"}
                )
                recovered_item = {
                    "type": "playlist",
                    "item": playlist,
                }
            else:
                playlist = PlaylistTable.get_by_id(item["hash"])
                if playlist is None:
                    continue

                tracks = TrackStore.get_tracks_by_trackhashes(playlist.trackhashes)
                playlist.clear_lists()

                if not playlist.has_image:
                    images = get_first_4_images(tracks)
                    images = [i["image"] for i in images]
                    playlist.images = images

                recovered_item = {
                    "type": "playlist",
                    "item": serialize_playlist(playlist),
                }
        elif item["type"] == "favorite":
            recovered_item = {
                "type": "favorite",
                "item": {
                    "count": FavoritesTable.count(),
                },
            }
        elif item["type"] == "track":
            track = TrackStore.trackhashmap.get(item["hash"])
            if track is None:
                continue

            recovered_item = {
                "type": "track",
                "item": serialize_track(track.get_best()),
            }

        if recovered_item is not None:
            helptext = item.get("help_text") or item.get("type")
            secondary_text = item.get("secondary_text")

            if "secondary_text" in item:
                secondary_text = item["secondary_text"]
            elif "timestamp" in item:
                secondary_text = timestamp_to_time_passed(item["timestamp"])

            if helptext:
                recovered_item["item"]["help_text"] = helptext

            if secondary_text:
                recovered_item["item"]["time"] = secondary_text

            recovered.append(recovered_item)

    return recovered


def get_recently_played_playlist(limit: int = 100):
    playlist = Playlist(
        id="recentlyplayed",
        name="Recently Played",
        image=None,
        last_updated="Now",
        settings={},
        trackhashes=[],
    )

    tracks = TrackStore.get_recently_played(limit)
    date = datetime.fromtimestamp(tracks[0].lastplayed)
    playlist._last_updated = date_string_to_time_passed(create_new_date(date))

    images = get_first_4_images(tracks=tracks)
    playlist.images = images

    return playlist, tracks
