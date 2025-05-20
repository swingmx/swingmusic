import os
from swingmusic.db.userdata import PlaylistTable
from swingmusic.lib.home import find_mix
from swingmusic.lib.home.recentlyadded import get_recently_added_playlist
from swingmusic.lib.home.recentlyplayed import get_recently_played_playlist
from swingmusic.models.logger import TrackLog
from swingmusic.store.albums import AlbumStore
from swingmusic.store.artists import ArtistStore
from swingmusic.store.tracks import TrackStore


def create_items(entries: list[TrackLog], limit: int):
    custom_playlists = [
        {"name": "recentlyadded", "handler": get_recently_added_playlist},
        {"name": "recentlyplayed", "handler": get_recently_played_playlist},
    ]

    items = []
    added = set()

    for entry in entries:
        if len(items) >= limit:
            break

        if entry.source in added:
            continue

        added.add(entry.source)

        if entry.type == "mix":
            if not entry.type_src:
                continue

            splits = entry.type_src.split(".")

            try:
                mixid = splits[0]
                sourcehash = splits[1]
            except IndexError:
                continue

            # INFO: Get mix from homepage store
            mix = find_mix(mixid, sourcehash)
            if not mix:
                continue

            items.append(
                {
                    "type": "mix",
                    "hash": entry.type_src,
                    "timestamp": entry.timestamp,
                }
            )
            continue

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

    return items
