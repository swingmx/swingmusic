from typing import Any

from app.config import UserConfig
from app.models import Album as AlbumModel, Artist as ArtistModel, Track as TrackModel
from app.models.favorite import Favorite
from app.models.lastfm import SimilarArtist
from app.models.logger import TrackLog
from app.models.playlist import Playlist
from app.models.plugins import Plugin
from app.models.user import User


def track_to_dataclass(track: Any, config: UserConfig):
    return TrackModel(**track._asdict(), config=config)


def tracks_to_dataclasses(tracks: Any):
    return [track_to_dataclass(track, UserConfig()) for track in tracks]


def album_to_dataclass(album: Any):
    return AlbumModel(**album._asdict())


def albums_to_dataclasses(albums: Any):
    return [album_to_dataclass(album) for album in albums]


def artist_to_dataclass(artist: Any):
    return ArtistModel(**artist._asdict())


def artists_to_dataclasses(artists: Any):
    return [artist_to_dataclass(artist) for artist in artists]


# SECTION: User data helpers


def similar_artist_to_dataclass(entry: Any):
    entry_dict = entry._asdict()
    del entry_dict["id"]

    return SimilarArtist(**entry_dict)


def similar_artists_to_dataclass(entries: Any):
    return [similar_artist_to_dataclass(entry) for entry in entries]


def favorite_to_dataclass(entry: Any):
    entry_dict = entry._asdict()
    del entry_dict["id"]

    return Favorite(**entry_dict)


def favorites_to_dataclass(entries: Any):
    return [favorite_to_dataclass(entry) for entry in entries]


def user_to_dataclass(entry: Any):
    entry_dict = entry._asdict()
    return User(**entry_dict)


def user_to_dataclasses(entries: Any):
    return [user_to_dataclass(entry) for entry in entries]


def plugin_to_dataclass(entry: Any):
    entry_dict = entry._asdict()
    del entry_dict["id"]
    return Plugin(**entry_dict)


def plugin_to_dataclasses(entries: Any):
    return [plugin_to_dataclass(entry) for entry in entries]


def tracklog_to_dataclass(entry: Any):
    entry_dict = entry._asdict()
    return TrackLog(**entry_dict)


def tracklog_to_dataclasses(entries: Any):
    return [tracklog_to_dataclass(entry) for entry in entries]


def playlist_to_dataclass(entry: Any):
    entry_dict = entry._asdict()
    return Playlist(**entry_dict)


def playlists_to_dataclasses(entries: Any):
    return [playlist_to_dataclass(entry) for entry in entries]
