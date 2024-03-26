from typing import List, TypeVar

from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from pydantic import BaseModel, Field

from app.api.apischemas import GenericLimitSchema
from app.models import FavType
from app.settings import Defaults
from app.utils.bisection import use_bisection
from app.db.sqlite.favorite import SQLiteFavoriteMethods as favdb
from app.serializers.track import serialize_track, serialize_tracks
from app.serializers.artist import serialize_for_card as serialize_artist
from app.serializers.album import serialize_for_card, serialize_for_card_many

from app.store.albums import AlbumStore
from app.store.tracks import TrackStore
from app.store.artists import ArtistStore
from app.utils.dates import timestamp_to_time_passed

bp_tag = Tag(name="Favorites", description="Your favorite items")
api = APIBlueprint("favorites", __name__, url_prefix="/favorites", abp_tags=[bp_tag])


T = TypeVar("T")


def remove_none(items: List[T]) -> List[T]:
    return [i for i in items if i is not None]


class FavoritesAddBody(BaseModel):
    hash: str = Field(
        description="The hash of the item",
        min_length=Defaults.HASH_LENGTH,
        max_length=Defaults.HASH_LENGTH,
        example=Defaults.API_ALBUMHASH,
    )
    type: str = Field(description="The type of the item", example=FavType.album)


@api.post("/add")
def add_favorite(body: FavoritesAddBody):
    """
    Adds a favorite to the database.
    """
    itemhash = body.hash
    itemtype = body.type

    favdb.insert_one_favorite(itemtype, itemhash)

    if itemtype == FavType.track:
        TrackStore.make_track_fav(itemhash)

    return {"msg": "Added to favorites"}


@api.post("/remove")
def remove_favorite(body: FavoritesAddBody):
    """
    Removes a favorite from the database.
    """
    itemhash = body.hash
    itemtype = body.type

    favdb.delete_favorite(itemtype, itemhash)

    if itemtype == FavType.track:
        TrackStore.remove_track_from_fav(itemhash)

    return {"msg": "Removed from favorites"}


@api.get("/albums")
def get_favorite_albums(query: GenericLimitSchema):
    """
    Get favorite albums
    """
    limit = query.limit
    albums = favdb.get_fav_albums()
    albumhashes = [a[1] for a in albums]
    albumhashes.reverse()

    src_albums = sorted(AlbumStore.albums, key=lambda x: x.albumhash)

    fav_albums = use_bisection(src_albums, "albumhash", albumhashes)
    fav_albums = remove_none(fav_albums)

    if limit == 0:
        limit = len(albums)

    return {"albums": serialize_for_card_many(fav_albums[:limit])}


@api.get("/tracks")
def get_favorite_tracks(query: GenericLimitSchema):
    """
    Get favorite tracks
    """
    limit = query.limit
    tracks = favdb.get_fav_tracks()
    trackhashes = [t[1] for t in tracks]
    trackhashes.reverse()
    src_tracks = sorted(TrackStore.tracks, key=lambda x: x.trackhash)

    tracks = use_bisection(src_tracks, "trackhash", trackhashes)
    tracks = remove_none(tracks)

    if limit == 0:
        limit = len(tracks)

    return {"tracks": serialize_tracks(tracks[:limit])}


@api.get("/artists")
def get_favorite_artists(query: GenericLimitSchema):
    """
    Get favorite artists
    """
    limit = query.limit
    artists = favdb.get_fav_artists()
    artisthashes = [a[1] for a in artists]
    artisthashes.reverse()

    src_artists = sorted(ArtistStore.artists, key=lambda x: x.artisthash)

    artists = use_bisection(src_artists, "artisthash", artisthashes)
    artists = remove_none(artists)

    if limit == 0:
        limit = len(artists)

    return {"artists": artists[:limit]}


class GetAllFavoritesQuery(BaseModel):
    """
    Extending this class will give you a model with the `limit` field
    """

    track_limit: int = Field(
        description="The number of tracks to return",
        example=Defaults.API_CARD_LIMIT,
        default=Defaults.API_CARD_LIMIT,
    )

    album_limit: int = Field(
        description="The number of albums to return",
        example=Defaults.API_CARD_LIMIT,
        default=Defaults.API_CARD_LIMIT,
    )

    artist_limit: int = Field(
        description="The number of artists to return",
        example=Defaults.API_CARD_LIMIT,
        default=Defaults.API_CARD_LIMIT,
    )


@api.get("")
def get_all_favorites(query: GetAllFavoritesQuery):
    """
    Returns all the favorites in the database.
    """
    track_limit = query.track_limit
    album_limit = query.album_limit
    artist_limit = query.artist_limit

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
        # INFO: hash is [1], type is [2], timestamp is [3]
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

    tracks = use_bisection(src_tracks, "trackhash", tracks, limit=track_limit)
    albums = use_bisection(src_albums, "albumhash", albums, limit=album_limit)
    artists = use_bisection(src_artists, "artisthash", artists, limit=artist_limit)

    tracks = remove_none(tracks)
    albums = remove_none(albums)
    artists = remove_none(artists)

    recents = []
    # first_n = favs

    for fav in favs:
        # INFO: hash is [1], type is [2], timestamp is [3]
        if len(recents) >= largest:
            break

        if fav[2] == FavType.album:
            album = next((a for a in albums if a.albumhash == fav[1]), None)

            if album is None:
                continue

            album = serialize_for_card(album)
            album["help_text"] = "album"
            album["time"] = timestamp_to_time_passed(fav[3])

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
            artist["time"] = timestamp_to_time_passed(fav[3])

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
            track["time"] = timestamp_to_time_passed(fav[3])

            recents.append({"type": "track", "item": track})

    return {
        "recents": recents[:album_limit],
        "tracks": tracks[:track_limit],
        "albums": albums[:album_limit],
        "artists": artists[:artist_limit],
        "count": count,
    }


@api.get("/check")
def check_favorite(query: FavoritesAddBody):
    """
    Checks if a favorite exists in the database.
    """
    itemhash = query.hash
    itemtype = query.type
    exists = favdb.check_is_favorite(itemhash, itemtype)

    return {"is_favorite": exists}
