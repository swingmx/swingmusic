"""
Contains all the album routes.
"""

import random

from flask import Blueprint, request

from app.db.sqlite.albumcolors import SQLiteAlbumMethods as adb
from app.db.sqlite.favorite import SQLiteFavoriteMethods as favdb
from app.db.sqlite.lastfm.similar_artists import SQLiteLastFMSimilarArtists as lastfmdb
from app.lib.albumslib import sort_by_track_no
from app.models import FavType, Track
from app.serializers.album import serialize_for_card
from app.serializers.track import serialize_track
from app.store.albums import AlbumStore
from app.store.tracks import TrackStore
from app.utils.hashing import create_hash

get_albums_by_albumartist = adb.get_albums_by_albumartist
check_is_fav = favdb.check_is_favorite

api = Blueprint("album", __name__, url_prefix="")


@api.route("/album", methods=["POST"])
def get_album_tracks_and_info():
    """
    Returns all the tracks in the given album
    """

    data = request.get_json()
    error_msg = {"msg": "No hash provided"}

    if data is None:
        return error_msg, 400

    try:
        albumhash: str = data["albumhash"]
    except KeyError:
        return error_msg, 400

    error_msg = {"error": "Album not created yet."}
    album = AlbumStore.get_album_by_hash(albumhash)

    if album is None:
        return error_msg, 404

    tracks = TrackStore.get_tracks_by_albumhash(albumhash)

    if tracks is None:
        return error_msg, 404

    if len(tracks) == 0:
        return error_msg, 404

    def get_album_genres(tracks: list[Track]):
        genres = set()

        for track in tracks:
            if track.genre is not None:
                genres.update(track.genre)

        return list(genres)

    album.genres = get_album_genres(tracks)
    album.count = len(tracks)

    album.get_date_from_tracks(tracks)
    album.duration = sum(t.duration for t in tracks)

    album.check_is_single(tracks)

    if not album.is_single:
        album.check_type()

    album.is_favorite = check_is_fav(albumhash, FavType.album)

    return {
        "tracks": [serialize_track(t, remove_disc=False) for t in tracks],
        "info": album,
    }


@api.route("/album/<albumhash>/tracks", methods=["GET"])
def get_album_tracks(albumhash: str):
    """
    Returns all the tracks in the given album, sorted by disc and track number.
    """
    tracks = TrackStore.get_tracks_by_albumhash(albumhash)
    tracks = sort_by_track_no(tracks)

    return {"tracks": tracks}


@api.route("/album/from-artist", methods=["POST"])
def get_artist_albums():
    data = request.get_json()

    if data is None:
        return {"msg": "No albumartist provided"}

    albumartists: str = data["albumartists"]
    limit: int = data.get("limit")
    base_title: str = data.get("base_title")

    albumartists: list[str] = albumartists.split(",")

    albums = [
        {
            "artisthash": a,
            "albums": AlbumStore.get_albums_by_albumartist(
                a, limit, exclude=base_title
            ),
        }
        for a in albumartists
    ]

    albums = [
        {
            "artisthash": a["artisthash"],
            "albums": [serialize_for_card(a_) for a_ in (a["albums"])],
        }
        for a in albums
        if len(a["albums"]) > 0
    ]

    return {"data": albums}


@api.route("/album/versions", methods=["POST"])
def get_album_versions():
    """
    Returns other versions of the given album.
    """

    data = request.get_json()

    if data is None:
        return {"msg": "No albumartist provided"}

    og_album_title: str = data["og_album_title"]
    base_title: str = data["base_title"]
    artisthash: str = data["artisthash"]

    albums = AlbumStore.get_albums_by_artisthash(artisthash)

    albums = [
        a
        for a in albums
        if create_hash(a.base_title) == create_hash(base_title)
        and create_hash(og_album_title) != create_hash(a.og_title)
    ]

    for a in albums:
        tracks = TrackStore.get_tracks_by_albumhash(a.albumhash)
        a.get_date_from_tracks(tracks)

    return {"data": albums}


@api.route("/album/similar", methods=["GET"])
def get_similar_albums():
    """
    Returns similar albums to the given album.
    """
    data = request.args

    if data is None:
        return {"msg": "No artisthash provided"}

    artisthash: str = data["artisthash"]
    limit: int = data.get("limit")

    if limit is None:
        limit = 6

    limit = int(limit)

    similar_artists = lastfmdb.get_similar_artists_for(artisthash)

    if similar_artists is None:
        return {"albums": []}

    artisthashes = similar_artists.get_artist_hash_set()

    if len(artisthashes) == 0:
        return {"albums": []}

    albums = [AlbumStore.get_albums_by_artisthash(a) for a in artisthashes]

    albums = [a for sublist in albums for a in sublist]
    albums = list({a.albumhash: a for a in albums}.values())

    try:
        albums = random.sample(albums, min(len(albums), limit))
    except ValueError:
        pass

    return {"albums": [serialize_for_card(a) for a in albums[:limit]]}
