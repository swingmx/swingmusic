"""
Contains all the album routes.
"""
from dataclasses import asdict

from flask import Blueprint
from flask import request

from app import utils
from app.db.sqlite.albums import SQLiteAlbumMethods as adb
from app.db.sqlite.favorite import SQLiteFavoriteMethods as favdb
from app.db.store import Store
from app.models import FavType
from app.models import Track

get_album_by_id = adb.get_album_by_id
get_albums_by_albumartist = adb.get_albums_by_albumartist
check_is_fav = favdb.check_is_favorite

albumbp = Blueprint("album", __name__, url_prefix="")


@albumbp.route("/album", methods=["POST"])
def get_album():
    """Returns all the tracks in the given album."""

    data = request.get_json()
    error_msg = {"msg": "No hash provided"}

    if data is None:
        return error_msg, 400

    try:
        albumhash = data["hash"]
    except KeyError:
        return error_msg, 400

    error_msg = {"error": "Album not created yet."}
    album = Store.get_album_by_hash(albumhash)

    if album is None:
        return error_msg, 204

    tracks = Store.get_tracks_by_albumhash(albumhash)

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
    tracks = utils.remove_duplicates(tracks)

    album.count = len(tracks)

    for track in tracks:
        if track.date != "Unknown":
            album.date = track.date
            break

    try:
        album.duration = sum((t.duration for t in tracks))
    except AttributeError:
        album.duration = 0

    if (
        album.count == 1
        and tracks[0].title == album.title
        # and tracks[0].track == 1
        # and tracks[0].disc == 1
    ):
        album.is_single = True
    else:
        album.check_type()

    album.is_favorite = check_is_fav(albumhash, FavType.album)

    return {"tracks": tracks, "info": album}


@albumbp.route("/album/<albumhash>/tracks", methods=["GET"])
def get_album_tracks(albumhash: str):
    """
    Returns all the tracks in the given album.
    """
    tracks = Store.get_tracks_by_albumhash(albumhash)
    tracks = [asdict(t) for t in tracks]

    for t in tracks:
        track = str(t["track"]).zfill(3)
        t["pos"] = int(f"{t['disc']}{track}")

    tracks = sorted(tracks, key=lambda t: t["pos"])

    return {"tracks": tracks}


@albumbp.route("/album/from-artist", methods=["POST"])
def get_artist_albums():
    data = request.get_json()

    if data is None:
        return {"msg": "No albumartist provided"}

    albumartists: str = data["albumartists"]  # type: ignore
    limit: int = data.get("limit")
    exclude: str = data.get("exclude")

    albumartists: list[str] = albumartists.split(",")  # type: ignore

    albums = [
        {
            "artisthash": a,
            "albums": Store.get_albums_by_albumartist(a, limit, exclude=exclude),
        }
        for a in albumartists
    ]

    albums = [a for a in albums if len(a["albums"]) > 0]

    return {"data": albums}


# @album_bp.route("/album/bio", methods=["POST"])
# def get_album_bio():
#     """Returns the album bio for the given album."""
#     data = request.get_json()
#     album_hash = data["hash"]
#     err_msg = {"bio": "No bio found"}

#     album = instances.album_instance.find_album_by_hash(album_hash)

#     if album is None:
#         return err_msg, 404

#     bio = FetchAlbumBio(album["title"], album["artist"])()

#     if bio is None:
#         return err_msg, 404

#     return {"bio": bio}
