from flask import Blueprint
from flask import request

from app.db.sqlite.favorite import SQLiteFavoriteMethods as favdb
from app.db.store import Store
from app.models import FavType
from app.utils import UseBisection

favbp = Blueprint("favorite", __name__, url_prefix="/")


def remove_none(items: list):
    return [i for i in items if i is not None]


@favbp.route("/favorite/add", methods=["POST"])
def add_favorite():
    """
    Adds a favorite to the database.
    """
    data = request.get_json()

    if data is None:
        return {"error": "No data provided"}, 400

    itemhash = data.get("hash")
    itemtype = data.get("type")

    favdb.insert_one_favorite(itemtype, itemhash)

    if itemtype == FavType.track:
        Store.add_fav_track(itemhash)

    return {"msg": "Added to favorites"}


@favbp.route("/favorite/remove", methods=["POST"])
def remove_favorite():
    """
    Removes a favorite from the database.
    """
    data = request.get_json()

    if data is None:
        return {"error": "No data provided"}, 400

    itemhash = data.get("hash")
    itemtype = data.get("type")

    favdb.delete_favorite(itemtype, itemhash)

    if itemtype == FavType.track:
        Store.remove_fav_track(itemhash)

    return {"msg": "Removed from favorites"}


@favbp.route("/albums/favorite")
def get_favorite_albums():
    limit = request.args.get("limit")

    if limit is None:
        limit = 6

    limit = int(limit)

    albums = favdb.get_fav_albums()
    albumhashes = [a[1] for a in albums]
    albumhashes.reverse()

    src_albums = sorted(Store.albums, key=lambda x: x.albumhash)

    fav_albums = UseBisection(src_albums, "albumhash", albumhashes)()
    fav_albums = remove_none(fav_albums)

    if limit == 0:
        limit = len(albums)

    return {"albums": fav_albums[:limit]}


@favbp.route("/tracks/favorite")
def get_favorite_tracks():
    limit = request.args.get("limit")

    if limit is None:
        limit = 6

    limit = int(limit)

    tracks = favdb.get_fav_tracks()
    trackhashes = [t[1] for t in tracks]
    trackhashes.reverse()
    src_tracks = sorted(Store.tracks, key=lambda x: x.trackhash)

    tracks = UseBisection(src_tracks, "trackhash", trackhashes)()
    tracks = remove_none(tracks)

    if limit == 0:
        limit = len(tracks)

    return {"tracks": tracks[:limit]}


@favbp.route("/artists/favorite")
def get_favorite_artists():
    limit = request.args.get("limit")

    if limit is None:
        limit = 6

    limit = int(limit)

    artists = favdb.get_fav_artists()
    artisthashes = [a[1] for a in artists]
    artisthashes.reverse()

    src_artists = sorted(Store.artists, key=lambda x: x.artisthash)

    artists = UseBisection(src_artists, "artisthash", artisthashes)()
    artists = remove_none(artists)

    if limit == 0:
        limit = len(artists)

    return {"artists": artists[:limit]}


@favbp.route("/favorites")
def get_all_favorites():
    """
    Returns all the favorites in the database.
    """
    track_limit = request.args.get("track_limit")
    album_limit = request.args.get("album_limit")
    artist_limit = request.args.get("artist_limit")

    if track_limit is None:
        track_limit = 6

    if album_limit is None:
        album_limit = 6

    if artist_limit is None:
        artist_limit = 6

    track_limit = int(track_limit)
    album_limit = int(album_limit)
    artist_limit = int(artist_limit)

    favs = favdb.get_all()
    favs.reverse()

    tracks = []
    albums = []
    artists = []

    for fav in favs:
        if (len(tracks) >= track_limit and len(albums) >= album_limit
                and len(artists) >= artist_limit):
            break

        if fav[2] == FavType.track:
            tracks.append(fav[1])
        elif fav[2] == FavType.album:
            albums.append(fav[1])
        elif fav[2] == FavType.artist:
            artists.append(fav[1])

    src_tracks = sorted(Store.tracks, key=lambda x: x.trackhash)
    src_albums = sorted(Store.albums, key=lambda x: x.albumhash)
    src_artists = sorted(Store.artists, key=lambda x: x.artisthash)

    tracks = tracks[:track_limit]
    albums = albums[:album_limit]
    artists = artists[:artist_limit]

    tracks = UseBisection(src_tracks, "trackhash", tracks)()
    albums = UseBisection(src_albums, "albumhash", albums)()
    artists = UseBisection(src_artists, "artisthash", artists)()

    tracks = remove_none(tracks)
    albums = remove_none(albums)
    artists = remove_none(artists)

    return {
        "tracks": tracks,
        "albums": albums,
        "artists": artists,
    }


@favbp.route("/favorites/check")
def check_favorite():
    """
    Checks if a favorite exists in the database.
    """
    itemhash = request.args.get("hash")
    itemtype = request.args.get("type")

    if itemhash is None:
        return {"error": "No hash provided"}, 400

    if itemtype is None:
        return {"error": "No type provided"}, 400

    exists = favdb.check_is_favorite(itemhash, itemtype)

    return {"is_favorite": exists}
