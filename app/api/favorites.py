from typing import List, TypeVar

from flask_jwt_extended import current_user
from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from pydantic import BaseModel, Field

from app.api.apischemas import GenericLimitSchema
from app.db.libdata import ArtistTable
from app.db.libdata import AlbumTable, TrackTable
from app.db.userdata import FavoritesTable
from app.models import FavType
from app.settings import Defaults
from app.utils.bisection import use_bisection
from app.serializers.track import serialize_track, serialize_tracks
from app.serializers.artist import (
    serialize_for_card as serialize_artist,
    serialize_for_cards,
)
from app.utils.dates import timestamp_to_time_passed
from app.serializers.album import serialize_for_card, serialize_for_card_many

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
def toggle_favorite(body: FavoritesAddBody):
    """
    Adds a favorite to the database.
    """
    FavoritesTable.insert_item({"hash": body.hash, "type": body.type})

    if body.type == FavType.track:
        TrackTable.set_is_favorite(body.hash, True)
    elif body.type == FavType.album:
        AlbumTable.set_is_favorite(body.hash, True)
    elif body.type == FavType.artist:
        ArtistTable.set_is_favorite(body.hash, True)

    return {"msg": "Added to favorites"}


@api.post("/remove")
def remove_favorite(body: FavoritesAddBody):
    """
    Removes a favorite from the database.
    """
    FavoritesTable.remove_item({"hash": body.hash, "type": body.type})

    if body.type == FavType.track:
        TrackTable.set_is_favorite(body.hash, False)
    elif body.type == FavType.album:
        AlbumTable.set_is_favorite(body.hash, False)
    elif body.type == FavType.artist:
        ArtistTable.set_is_favorite(body.hash, False)

    return {"msg": "Removed from favorites"}


class GetAllOfTypeQuery(GenericLimitSchema):
    """
    Extending this class will give you a model with the `limit` field
    """

    start: int = Field(
        description="Where to start from",
        example=Defaults.API_CARD_LIMIT,
        default=Defaults.API_CARD_LIMIT,
    )


@api.get("/albums")
def get_favorite_albums(query: GetAllOfTypeQuery):
    """
    Get favorite albums
    """
    fav_albums, total = FavoritesTable.get_fav_albums(query.start, query.limit)
    fav_albums.reverse()

    return {"albums": serialize_for_card_many(fav_albums), "total": total}


@api.get("/tracks")
def get_favorite_tracks(query: GetAllOfTypeQuery):
    """
    Get favorite tracks
    """
    tracks, total = FavoritesTable.get_fav_tracks(query.start, query.limit)
    return {"tracks": serialize_tracks(tracks), "total": total}


@api.get("/artists")
def get_favorite_artists(query: GetAllOfTypeQuery):
    """
    Get favorite artists
    """
    artists, total = FavoritesTable.get_fav_artists(
        start=query.start,
        limit=query.limit,
    )
    artists.reverse()

    return {"artists": [serialize_artist(a) for a in artists], "total": total}


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

    favs = FavoritesTable.get_all()
    favs.reverse()

    tracks = []
    albums = []
    artists = []

    track_master_hash = TrackTable.get_all_hashes()
    album_master_hash = AlbumTable.get_all_hashes()
    artist_master_hash = ArtistTable.get_all_hashes()

    # INFO: Filter out invalid hashes (file not found or tags edited)
    for fav in favs:
        hash = fav.hash
        type = fav.type

        if type == FavType.track:
            tracks.append(hash) if hash in track_master_hash else None

        if type == FavType.artist:
            artists.append(hash) if hash in artist_master_hash else None

        if type == FavType.album:
            albums.append(hash) if hash in album_master_hash else None

    count = {
        "tracks": len(tracks),
        "albums": len(albums),
        "artists": len(artists),
    }

    tracks = TrackTable.get_tracks_by_trackhashes(tracks, limit=track_limit)
    albums = AlbumTable.get_albums_by_albumhashes(albums, limit=album_limit)
    artists = ArtistTable.get_artists_by_artisthashes(artists, limit=artist_limit)

    recents = []
    # first_n = favs

    for fav in favs:
        if len(recents) >= largest:
            break

        if fav.type == FavType.album:
            album = next((a for a in albums if a.albumhash == fav.hash), None)

            if album is None:
                continue

            album = serialize_for_card(album)
            album["help_text"] = "album"
            album["time"] = timestamp_to_time_passed(fav.timestamp)

            recents.append(
                {
                    "type": "album",
                    "item": album,
                }
            )

        if fav.type == FavType.artist:
            artist = next((a for a in artists if a.artisthash == fav.hash), None)

            if artist is None:
                continue

            artist = serialize_artist(artist)
            artist["help_text"] = "artist"
            artist["time"] = timestamp_to_time_passed(fav.timestamp)

            recents.append(
                {
                    "type": "artist",
                    "item": artist,
                }
            )

        if fav.type == FavType.track:
            track = next((t for t in tracks if t.trackhash == fav.hash), None)

            if track is None:
                continue

            track = serialize_track(track)
            track["help_text"] = "track"
            track["time"] = timestamp_to_time_passed(fav.timestamp)

            recents.append({"type": "track", "item": track})

    return {
        "recents": recents[:album_limit],
        "tracks": serialize_tracks(tracks[:track_limit]),
        "albums": serialize_for_card_many(albums[:album_limit]),
        "artists": serialize_for_cards(artists[:artist_limit]),
        "count": count,
    }


@api.get("/check")
def check_favorite(query: FavoritesAddBody):
    """
    Checks if a favorite exists in the database.
    """
    itemhash = query.hash
    itemtype = query.type

    return {"is_favorite": FavoritesTable.check_exists(itemhash, itemtype)}
