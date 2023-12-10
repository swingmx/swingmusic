import os
from app.models.logger import Track as TrackLog

from app.db.sqlite.logger.tracks import SQLiteTrackLogger as db
from app.db.sqlite.playlists import SQLitePlaylistMethods as pdb
from app.db.sqlite.favorite import SQLiteFavoriteMethods as fdb

from app.serializers.track import serialize_track
from app.serializers.album import album_serializer
from app.serializers.artist import serialize_for_card
from app.serializers.playlist import serialize_for_card as serialize_playlist
from app.lib.playlistlib import get_first_4_images, get_recently_added_playlist

from app.store.albums import AlbumStore
from app.store.tracks import TrackStore
from app.store.artists import ArtistStore


def get_recently_played(limit=7):
    entries = db.get_all()
    items = []
    added = set()

    for entry in entries:
        if len(items) >= limit:
            break

        entry = TrackLog(*entry)

        if entry.source in added:
            continue

        added.add(entry.source)

        if entry.type == "album":
            album = AlbumStore.get_album_by_hash(entry.type_src)

            if album is None:
                continue

            album = album_serializer(
                album,
                {
                    "genres",
                    "date",
                    "count",
                    "duration",
                    "albumartists_hashes",
                    "og_title",
                },
            )
            album["help_text"] = "album"

            items.append({"type": "album", "item": album})
            continue

        if entry.type == "artist":
            artist = ArtistStore.get_artist_by_hash(entry.type_src)

            if artist is None:
                continue

            artist = serialize_for_card(artist)
            artist["help_text"] = "artist"

            items.append({"type": "artist", "item": artist})

            continue

        if entry.type == "folder":
            folder = entry.type_src
            if not folder:
                continue

            is_home_dir = entry.type_src == "$home"

            if is_home_dir:
                folder = os.path.expanduser("~")

            count = len([t for t in TrackStore.tracks if t.folder == folder])
            items.append(
                {
                    "type": "folder",
                    "item": {
                        "path": entry.type_src,
                        "count": count,
                        "help_text": "folder",
                    },
                }
            )
            continue

        if entry.type == "playlist":
            is_recently_added = entry.type_src == "recentlyadded"

            if is_recently_added:
                playlist, _ = get_recently_added_playlist()
                playlist.images = [i["image"] for i in playlist.images]

                playlist = serialize_playlist(
                    playlist, to_remove={"settings", "duration"}
                )

                playlist["help_text"] = "playlist"
                items.append(
                    {
                        "type": "playlist",
                        "item": playlist,
                    }
                )
                continue

            playlist = pdb.get_playlist_by_id(entry.type_src)
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
                    "item": {"help_text": "playlist", **serialize_playlist(playlist)},
                }
            )

        if entry.type == "favorite":
            items.append(
                {
                    "type": "favorite_tracks",
                    "item": {
                        "help_text": "playlist",
                        "count": fdb.get_track_count(),
                    },
                }
            )
            continue

        try:
            track = TrackStore.get_tracks_by_trackhashes([entry.trackhash])[0]
        except IndexError:
            continue

        track = serialize_track(track)
        track["help_text"] = "track"

        items.append({"type": "track", "item": track})

    return items
