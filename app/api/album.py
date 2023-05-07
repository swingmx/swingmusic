"""
Contains all the album routes.
"""

from dataclasses import asdict

from flask import Blueprint, request

from app.db.sqlite.albums import SQLiteAlbumMethods as adb
from app.db.sqlite.favorite import SQLiteFavoriteMethods as favdb
from app.models import FavType, Track
from app.utils.hashing import create_hash
from app.utils.remove_duplicates import remove_duplicates

from app.store.tracks import TrackStore
from app.store.albums import AlbumStore

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
        albumhash = data["hash"]
    except KeyError:
        return error_msg, 400

    error_msg = {"error": "Album not created yet."}
    album = AlbumStore.get_album_by_hash(albumhash)

    if album is None:
        return error_msg, 204

    tracks = TrackStore.get_tracks_by_albumhash(albumhash)

    if tracks is None:
        return error_msg, 404

    if len(tracks) == 0:
        return error_msg, 204

    def get_album_genres(tracks: list[Track]):
        genres = set()

        for track in tracks:
            if track.genre is not None:
                genres.update(track.genre)

        return list(genres)

    album.genres = get_album_genres(tracks)
    tracks = remove_duplicates(tracks)

    album.count = len(tracks)
    album.get_date_from_tracks(tracks)

    try:
        album.duration = sum((t.duration for t in tracks))
    except AttributeError:
        album.duration = 0

    album.check_is_single(tracks)

    if not album.is_single:
        album.check_type()

    album.is_favorite = check_is_fav(albumhash, FavType.album)

    return {"tracks": tracks, "info": album}


@api.route("/album/<albumhash>/tracks", methods=["GET"])
def get_album_tracks(albumhash: str):
    """
    Returns all the tracks in the given album, sorted by disc and track number.
    """
    tracks = TrackStore.get_tracks_by_albumhash(albumhash)
    tracks = [asdict(t) for t in tracks]

    for t in tracks:
        track = str(t["track"]).zfill(3)
        t["pos"] = int(f"{t['disc']}{track}")

    tracks = sorted(tracks, key=lambda t: t["pos"])

    return {"tracks": tracks}


@api.route("/album/from-artist", methods=["POST"])
def get_artist_albums():
    data = request.get_json()

    if data is None:
        return {"msg": "No albumartist provided"}

    albumartists: str = data["albumartists"]
    limit: int = data.get("limit")
    exclude: str = data.get("exclude")

    albumartists: list[str] = albumartists.split(",")

    albums = [
        {
            "artisthash": a,
            "albums": AlbumStore.get_albums_by_albumartist(a, limit, exclude=exclude),
        }
        for a in albumartists
    ]

    albums = [a for a in albums if len(a["albums"]) > 0]

    return {"data": albums}


@api.route("/album/versions", methods=["POST"])
def get_album_versions():
    """
    Returns other versions of the given album.
    """

    data = request.get_json()

    if data is None:
        return {"msg": "No albumartist provided"}

    og_album_title: str = data['og_album_title']
    base_title: str = data['base_title']
    artisthash: str = data['artisthash']

    albums = AlbumStore.get_albums_by_artisthash(artisthash)
    print(base_title, artisthash)

    albums = [
        a for a in albums
        if
        create_hash(a.base_title) == create_hash(base_title) and create_hash(og_album_title) != create_hash(a.og_title)
    ]

    print(albums)

    return {
        "data": albums
    }
