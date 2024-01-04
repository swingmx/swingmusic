from flask import Blueprint, request

from app.db.sqlite.favorite import SQLiteFavoriteMethods as favdb
from app.models import FavType
from app.serializers.album import serialize_for_card, serialize_for_card_many
from app.serializers.artist import serialize_for_card as serialize_artist
from app.serializers.track import serialize_track, serialize_tracks
from app.utils.bisection import UseBisection

from app.store.artists import ArtistStore
from app.store.albums import AlbumStore
from app.store.tracks import TrackStore


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

    return {"albums": serialize_for_card_many(fav_albums[:limit])}


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

    return {"tracks": serialize_tracks(tracks[:limit])}


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

    # largest is x2 to accound for broken hashes if any
    largest = max(track_limit, album_limit, artist_limit)

    favs = favdb.get_all()
    favs.reverse()

    tracks = []
    albums = []
    artists = []

    track_master_hash = set(t.trackhash for t in TrackStore.tracks)
    album_master_hash = set(a.albumhash for a in AlbumStore.albums)
    artist_master_hash = set(a.artisthash for a in ArtistStore.artists)

    for fav in favs:
        hash = fav[1]
        if fav[2] == FavType.track:
            tracks.append(hash) if hash in track_master_hash else None

        if fav[2] == FavType.artist:
            artists.append(hash) if hash in artist_master_hash else None

        if fav[2] == FavType.album:
            albums.append(hash) if hash in album_master_hash else None

    count = {
        "tracks": len(tracks),
        "albums": len(albums),
        "artists": len(artists),
    }

    src_tracks = sorted(TrackStore.tracks, key=lambda x: x.trackhash)
    src_albums = sorted(AlbumStore.albums, key=lambda x: x.albumhash)
    src_artists = sorted(ArtistStore.artists, key=lambda x: x.artisthash)

    tracks = UseBisection(src_tracks, "trackhash", tracks, limit=track_limit)()
    albums = UseBisection(src_albums, "albumhash", albums, limit=album_limit)()
    artists = UseBisection(src_artists, "artisthash", artists, limit=artist_limit)()

    tracks = remove_none(tracks)
    albums = remove_none(albums)
    artists = remove_none(artists)

    recents = []
    # first_n = favs

    for fav in favs:
        if len(recents) >= largest:
            break

        if fav[2] == FavType.album:
            album = next((a for a in albums if a.albumhash == fav[1]), None)

            if album is None:
                continue

            album = serialize_for_card(album)
            album["help_text"] = "album"

            recents.append(
                {
                    "type": "album",
                    "item": album,
                }
            )

        if fav[2] == FavType.artist:
            artist = next((a for a in artists if a.artisthash == fav[1]), None)

            if artist is None:
                continue

            artist = serialize_artist(artist)
            artist["help_text"] = "artist"

            recents.append(
                {
                    "type": "artist",
                    "item": artist,
                }
            )

        if fav[2] == FavType.track:
            track = next((t for t in tracks if t.trackhash == fav[1]), None)

            if track is None:
                continue

            track = serialize_track(track)
            track["help_text"] = "track"

            recents.append({"type": "track", "item": track})

    return {
        "recents": recents[:album_limit],
        "tracks": tracks[:track_limit],
        "albums": albums[:album_limit],
        "artists": artists[:artist_limit],
        "count": count,
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
