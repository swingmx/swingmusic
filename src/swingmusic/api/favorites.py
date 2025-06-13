from typing import List, TypeVar

from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from pydantic import BaseModel, Field

from swingmusic.api.apischemas import GenericLimitSchema
from swingmusic.db.userdata import FavoritesTable
from swingmusic.lib.extras import get_extra_info
from swingmusic.models import FavType
from swingmusic.settings import Defaults

from swingmusic.store.albums import AlbumStore
from swingmusic.store.artists import ArtistStore
from swingmusic.store.tracks import TrackStore

from swingmusic.serializers.track import serialize_track, serialize_tracks
from swingmusic.serializers.artist import (
    serialize_for_card as serialize_artist,
    serialize_for_cards,
)
from swingmusic.utils.dates import timestamp_to_time_passed
from swingmusic.serializers.album import serialize_for_card, serialize_for_card_many

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
    )
    type: str = Field(description="The type of the item")


def toggle_fav(type: str, hash: str):
    """
    Toggles a favorite item.
    """
    if type == FavType.track:
        entry = TrackStore.trackhashmap.get(hash)
        if entry is not None:
            entry.toggle_favorite_user()

    elif type == FavType.album:
        entry = AlbumStore.albummap.get(hash)

        if entry is not None:
            entry.toggle_favorite_user()
    elif type == FavType.artist:
        entry = ArtistStore.artistmap.get(hash)

        if entry is not None:
            entry.toggle_favorite_user()

    return {"msg": "Added to favorites"}


@api.post("/add")
def toggle_favorite(body: FavoritesAddBody):
    """
    Adds a favorite to the database.
    """
    extra = get_extra_info(body.hash, body.type)

    try:
        FavoritesTable.insert_item(
            {"hash": body.hash, "type": body.type, "extra": extra}
        )
    except Exception as e:
        print(e)
        return {"msg": "Failed! An error occured"}, 500

    toggle_fav(body.type, body.hash)

    return {"msg": "Added to favorites"}


@api.post("/remove")
def remove_favorite(body: FavoritesAddBody):
    """
    Removes a favorite from the database.
    """
    try:
        FavoritesTable.remove_item({"hash": body.hash, "type": body.type})
    except Exception as e:
        print(e)
        return {"msg": "Failed! An error occured"}, 500

    toggle_fav(body.type, body.hash)

    return {"msg": "Removed from favorites"}


class GetAllOfTypeQuery(GenericLimitSchema):
    """
    Extending this class will give you a model with the `limit` field
    """

    start: int = Field(
        description="Where to start from",
        default=Defaults.API_CARD_LIMIT,
    )


@api.get("/albums")
def get_favorite_albums(query: GetAllOfTypeQuery):
    """
    Get favorite albums

    Note: Only the first request will return the total number of favorites.
    Others will return -1
    """
    fav_albums, total = FavoritesTable.get_fav_albums(query.start, query.limit)
    albums = AlbumStore.get_albums_by_hashes(a.hash for a in fav_albums)

    return {"albums": serialize_for_card_many(albums), "total": total}


@api.get("/tracks")
def get_favorite_tracks(query: GetAllOfTypeQuery):
    """
    Get favorite tracks

    Note: Only the first request will return the total number of favorites.
    Others will return -1
    """
    tracks, total = FavoritesTable.get_fav_tracks(query.start, query.limit)
    tracks = TrackStore.get_tracks_by_trackhashes([t.hash for t in tracks])

    return {"tracks": serialize_tracks(tracks), "total": total}


@api.get("/artists")
def get_favorite_artists(query: GetAllOfTypeQuery):
    """
    Get favorite artists

    Note: Only the first request will return the total number of favorites.
    Others will return -1
    """
    artists, total = FavoritesTable.get_fav_artists(
        start=query.start,
        limit=query.limit,
    )

    artists = ArtistStore.get_artists_by_hashes(a.hash for a in artists)
    return {"artists": [serialize_artist(a) for a in artists], "total": total}


class GetAllFavoritesQuery(BaseModel):
    """
    Extending this class will give you a model with the `limit` field
    """

    track_limit: int = Field(
        description="The number of tracks to return",
        default=Defaults.API_CARD_LIMIT,
    )

    album_limit: int = Field(
        description="The number of albums to return",
        default=Defaults.API_CARD_LIMIT,
    )

    artist_limit: int = Field(
        description="The number of artists to return",
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

    favs = FavoritesTable.get_all(with_user=True)
    favs = sorted(favs, key=lambda x: x.timestamp, reverse=True)

    tracks = []
    albums = []
    artists = []

    track_master_hash = TrackStore.trackhashmap.keys()
    album_master_hash = AlbumStore.albummap.keys()
    artist_master_hash = ArtistStore.artistmap.keys()

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

    tracks = TrackStore.get_tracks_by_trackhashes(tracks[:track_limit])
    albums = AlbumStore.get_albums_by_hashes(albums[:album_limit])
    artists = ArtistStore.get_artists_by_hashes(artists[:artist_limit])

    recents = []

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
