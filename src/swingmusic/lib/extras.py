from typing import Any
from swingmusic.store.albums import AlbumStore
from swingmusic.store.artists import ArtistStore
from swingmusic.store.tracks import TrackStore


def get_extra_info(hash: str, type: str):
    """
    Generates extra info for a track, album or artist, which will be stored
    in the database (in favorites, playlists and scrobble data) for backup and restore.

    The extra info contains all the fields needed to reconstruct the itemhash. The track contains an additional filepath field which can be used to locate the file when restoring.
    """
    extra: dict[str, Any] = {}

    if type == "track":
        trackentry = TrackStore.trackhashmap.get(hash)
        if trackentry is not None:
            track = trackentry.get_best()

            extra["filepath"] = track.filepath
            extra["title"] = track.title
            extra["artists"] = [a["name"] for a in track.artists]
            extra["album"] = track.albumhash

    elif type == "album":
        album = AlbumStore.get_album_by_hash(hash)
        if album is not None:
            extra["albumartists"] = [a["name"] for a in album.albumartists]
            extra["title"] = album.title

    elif type == "artist":
        artist = ArtistStore.get_artist_by_hash(hash)
        if artist is not None:
            extra["name"] = artist.name

    return extra
