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


def get_recently_played(limit=7):
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
                album = AlbumStore.get_album_by_hash(entry.type_src)

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
                album["help_text"] = "album"
                album["time"] = timestamp_to_time_passed(entry.timestamp)

                items.append(
                    {
                        "type": "album",
                        "item": album,
                    }
                )
                continue

            if entry.type == "artist":
                artist = ArtistStore.get_artist_by_hash(entry.type_src)

                if artist is None:
                    continue

                artist = serialize_for_card(artist)
                artist["help_text"] = "artist"
                artist["time"] = timestamp_to_time_passed(entry.timestamp)

                items.append(
                    {
                        "type": "artist",
                        "item": artist,
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

                # print(folder)
                # folder = os.path.join("/", folder, "")
                # print(folder)
                # count = len([t for t in TrackStore.tracks if t.folder == folder])
                count = FolderStore.count_tracks_containing_paths([folder])
                items.append(
                    {
                        "type": "folder",
                        "item": {
                            "path": folder,
                            "count": count[0]["trackcount"],
                            "help_text": "folder",
                            "time": timestamp_to_time_passed(entry.timestamp),
                        },
                    }
                )
                continue

            if entry.type == "playlist":
                is_custom = entry.type_src in [i["name"] for i in custom_playlists]
                # is_recently_added = entry.type_src == "recentlyadded"

                if is_custom:
                    playlist, _ = next(
                        i["handler"]()
                        for i in custom_playlists
                        if i["name"] == entry.type_src
                    )
                    playlist.images = [i["image"] for i in playlist.images]

                    playlist = serialize_playlist(
                        playlist, to_remove={"settings", "duration"}
                    )

                    playlist["help_text"] = "playlist"
                    playlist["time"] = timestamp_to_time_passed(entry.timestamp)

                    items.append(
                        {
                            "type": "playlist",
                            "item": playlist,
                        }
                    )
                    continue

                playlist = PlaylistTable.get_by_id(entry.type_src)
                if playlist is None:
                    continue

                tracks = TrackStore.get_tracks_by_trackhashes(playlist.trackhashes)
                playlist.clear_lists()

                if not playlist.has_image:
                    images = get_first_4_images(tracks)
                    images = [i["image"] for i in images]
                    playlist.images = images

                items.append(
                    {
                        "type": "playlist",
                        "item": {
                            "help_text": "playlist",
                            "time": timestamp_to_time_passed(entry.timestamp),
                            **serialize_playlist(playlist),
                        },
                    }
                )

            if entry.type == "favorite":
                items.append(
                    {
                        "type": "favorite_tracks",
                        "item": {
                            "help_text": "playlist",
                            "count": FavoritesTable.count(),
                            "time": timestamp_to_time_passed(entry.timestamp),
                        },
                    }
                )
                continue

            t = TrackStore.trackhashmap.get(entry.trackhash)

            if t is None:
                continue

            track = serialize_track(t.get_best())
            track["help_text"] = "track"
            track["time"] = timestamp_to_time_passed(entry.timestamp)

            items.append(
                {
                    "type": "track",
                    "item": track,
                }
            )

    BATCH_SIZE = 200
    current_index = 0

    entries = ScrobbleTable.get_all(0, BATCH_SIZE)
    max_iterations = 20 # Safeguard against unexpected infinite loops
    iterations = 0

    while len(items) < limit and iterations < max_iterations:
        create_items(entries)
        current_index += BATCH_SIZE

        if len(items) < limit:
            entries = ScrobbleTable.get_all(current_index + 1, BATCH_SIZE)
            if not entries:
                break

        iterations += 1

    if iterations == max_iterations:
        print(
            f"Warning: Reached maximum iterations ({max_iterations}) while fetching recently played items"
        )

    return items


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
