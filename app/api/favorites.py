from flask import Blueprint, request

from app.db.sqlite.favorite import SQLiteFavoriteMethods as favdb
from app.models import FavType
from app.utils.bisection import UseBisection

from app.store.artists import ArtistStore
from app.store.albums import AlbumStore
from app.store.tracks import TrackStore
from app.serializers.favorites_serializer import recent_fav_track_serializer, recent_fav_album_serializer, \
    recent_fav_artist_serializer

api = Blueprint("favorite", __name__, url_prefix="/")


def remove_none(items: list):
    return [i for i in items if i is not None]


@api.route("/favorite/add", methods=["POST"])
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
        TrackStore.make_track_fav(itemhash)

    return {"msg": "Added to favorites"}


@api.route("/favorite/remove", methods=["POST"])
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
        TrackStore.remove_track_from_fav(itemhash)

    return {"msg": "Removed from favorites"}


@api.route("/albums/favorite")
def get_favorite_albums():
    limit = request.args.get("limit")

    if limit is None:
        limit = 6

    limit = int(limit)

    albums = favdb.get_fav_albums()
    albumhashes = [a[1] for a in albums]
    albumhashes.reverse()

    src_albums = sorted(AlbumStore.albums, key=lambda x: x.albumhash)

    fav_albums = UseBisection(src_albums, "albumhash", albumhashes)()
    fav_albums = remove_none(fav_albums)

    if limit == 0:
        limit = len(albums)

    return {"albums": fav_albums[:limit]}


@api.route("/tracks/favorite")
def get_favorite_tracks():
    limit = request.args.get("limit")

    if limit is None:
        limit = 6

    limit = int(limit)

    tracks = favdb.get_fav_tracks()
    trackhashes = [t[1] for t in tracks]
    trackhashes.reverse()
    src_tracks = sorted(TrackStore.tracks, key=lambda x: x.trackhash)

    tracks = UseBisection(src_tracks, "trackhash", trackhashes)()
    tracks = remove_none(tracks)

    if limit == 0:
        limit = len(tracks)

    return {"tracks": tracks[:limit]}


@api.route("/artists/favorite")
def get_favorite_artists():
    limit = request.args.get("limit")

    if limit is None:
        limit = 6

    limit = int(limit)

    artists = favdb.get_fav_artists()
    artisthashes = [a[1] for a in artists]
    artisthashes.reverse()

    src_artists = sorted(ArtistStore.artists, key=lambda x: x.artisthash)

    artists = UseBisection(src_artists, "artisthash", artisthashes)()
    artists = remove_none(artists)

    if limit == 0:
        limit = len(artists)

    return {"artists": artists[:limit]}


@api.route("/favorites")
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
        if (
                len(tracks) >= track_limit
                and len(albums) >= album_limit
                and len(artists) >= artist_limit
        ):
            break

        if not len(tracks) >= track_limit:
            if fav[2] == FavType.track:
                tracks.append(fav[1])

        if not len(albums) >= album_limit:
            if fav[2] == FavType.album:
                albums.append(fav[1])

        if not len(artists) >= artist_limit:
            if fav[2] == FavType.artist:
                artists.append(fav[1])

    src_tracks = sorted(TrackStore.tracks, key=lambda x: x.trackhash)
    src_albums = sorted(AlbumStore.albums, key=lambda x: x.albumhash)
    src_artists = sorted(ArtistStore.artists, key=lambda x: x.artisthash)

    tracks = UseBisection(src_tracks, "trackhash", tracks)()
    albums = UseBisection(src_albums, "albumhash", albums)()
    artists = UseBisection(src_artists, "artisthash", artists)()

    tracks = remove_none(tracks)
    albums = remove_none(albums)
    artists = remove_none(artists)

    recents = []
    first_n = favs[:album_limit]

    for fav in first_n:
        if fav[2] == FavType.track:
            track = [t for t in tracks if t.trackhash == fav[1]][0]
            recents.append({
                "type": "track",
                "item": recent_fav_track_serializer(track)
            })

        elif fav[2] == FavType.album:
            album = [a for a in albums if a.albumhash == fav[1]][0]
            recents.append({
                "type": "album",
                "item": recent_fav_album_serializer(album)
            })

        elif fav[2] == FavType.artist:
            artist = [a for a in artists if a.artisthash == fav[1]][0]
            recents.append({
                "type": "artist",
                "item": recent_fav_artist_serializer(artist)
            })

    return {
        "recents": recents,
        "tracks": tracks,
        "albums": albums,
        "artists": artists,
    }


@api.route("/favorites/check")
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
