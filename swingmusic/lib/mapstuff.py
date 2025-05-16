from swingmusic.db.userdata import LibDataTable, FavoritesTable, ScrobbleTable
from swingmusic.store.albums import AlbumStore
from swingmusic.store.artists import ArtistStore
from swingmusic.store.tracks import TrackStore


from typing import Any


def map_scrobble_data():
    """
    Maps scrobble data to the in-memory stores.

    The scrobble data is loaded from the database and grouped by trackhash.
    The album and artist scrobble data (for those tracks) are then incremented based on the data.
    """
    records = ScrobbleTable.get_all(0, None)

    # group records by trackhash
    grouped: dict[str, dict[str, Any]] = {}

    for record in records:
        # aggregate playcount, playduration and lastplayed
        item = grouped.setdefault(record.trackhash, {})
        item["playcount"] = item.get("playcount", 0) + 1
        item["playduration"] = item.get("playduration", 0) + record.duration
        item["lastplayed"] = max(item.get("lastplayed", 0), record.timestamp)

    # increment playcount, playduration and lastplayed for albums and artists
    for trackhash, data in grouped.items():
        track = TrackStore.trackhashmap.get(trackhash)

        if track is None:
            continue

        track.increment_playcount(
            data["playduration"], data["lastplayed"], data["playcount"]
        )

        album = AlbumStore.albummap.get(track.tracks[0].albumhash)
        if album:
            album.increment_playcount(
                data["playduration"], data["lastplayed"], data["playcount"]
            )

        for artisthash in track.tracks[0].artisthashes:
            artist = ArtistStore.artistmap.get(artisthash)
            if artist:
                artist.increment_playcount(
                    data["playduration"], data["lastplayed"], data["playcount"]
                )


def map_favorites():
    """
    Maps favorites data to the in-memory stores.
    """
    favorites = FavoritesTable.get_all()

    for entry in favorites:
        if entry.type == "album":
            album = AlbumStore.albummap.get(entry.hash)
            if album:
                album.toggle_favorite_user(entry.userid)

        elif entry.type == "artist":
            artist = ArtistStore.artistmap.get(entry.hash)
            if artist:
                artist.toggle_favorite_user(entry.userid)

        elif entry.type == "track":
            track = TrackStore.trackhashmap.get(entry.hash)
            if track:
                track.toggle_favorite_user(entry.userid)


def map_artist_colors():
    colors = LibDataTable.get_all_colors(type="artist")

    for color in colors:
        artist = ArtistStore.artistmap.get(color["itemhash"])

        if artist:
            artist.set_color(color["color"])


def map_album_colors():
    colors = LibDataTable.get_all_colors(type="album")

    for color in colors:
        album = AlbumStore.albummap.get(color["itemhash"])

        if album:
            album.set_color(color["color"])
