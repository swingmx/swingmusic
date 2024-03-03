"""
Contains all the album routes.
"""

from operator import length_hint
import random

from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from pydantic import BaseModel, Field

from app.db.sqlite.albumcolors import SQLiteAlbumMethods as adb
from app.db.sqlite.favorite import SQLiteFavoriteMethods as favdb
from app.db.sqlite.lastfm.similar_artists import SQLiteLastFMSimilarArtists as lastfmdb
from app.lib.albumslib import sort_by_track_no
from app.models import FavType, Track
from app.serializers.album import serialize_for_card
from app.serializers.track import serialize_track
from app.settings import Defaults
from app.store.albums import AlbumStore
from app.store.tracks import TrackStore
from app.utils.hashing import create_hash

get_albums_by_albumartist = adb.get_albums_by_albumartist
check_is_fav = favdb.check_is_favorite

book_tag = Tag(name="Album", description="Single album")
api = APIBlueprint("album", __name__, url_prefix="", abp_tags=[book_tag])


class GetAlbumBody(BaseModel):
    albumhash: str = Field(
        description="The hash of the album to get",
        example="49e4819273",
        min_length=Defaults.HASH_LENGTH,
        max_length=Defaults.HASH_LENGTH,
    )


@api.post("/album", summary="Get album")
def get_album_tracks_and_info(body: GetAlbumBody):
    """
    Returns album info and tracks for the given albumhash.
    """
    albumhash = body.albumhash

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

class GetAlbumTracksQuery(BaseModel):
    albumhash: str = Field(
        description="The hash of the album",
        example="49e4819273",
        min_length=Defaults.HASH_LENGTH,
        max_length=Defaults.HASH_LENGTH,
    )

@api.get("/album/<albumhash>/tracks", summary="Get album tracks")
def get_album_tracks(query: GetAlbumTracksQuery):
    """
    Returns all the tracks in the given album, sorted by disc and track number.
    """
    tracks = TrackStore.get_tracks_by_albumhash(query.albumhash)
    tracks = sort_by_track_no(tracks)

    return {"tracks": tracks}

class GetMoreFromArtistsBody(BaseModel):
    albumartists: str = Field(
        description="The artist hashes to get more albums from",
        example=Defaults.API_ARTISTHASH
    )
    limit: int = Field(
        description="The maximum number of albums to return per artist",
        example=7,
        default=7,
    )
    base_title: str = Field(
        description="The base title of the album to exclude from the results.",
        example=Defaults.API_ALBUMNAME,
        default=None,
    )

@api.post("/album/from-artist", summary="More from artist")
def get_more_from_artist(body: GetMoreFromArtistsBody):
    """
    Returns more albums from the given artist hashes.
    """
    albumartists = body.albumartists
    limit = body.limit
    base_title = body.base_title

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


class GetAlbumVersionsBody(BaseModel):
    og_album_title: str = Field(
        description="The original album title (album.og_title)",
        example=Defaults.API_ALBUMNAME,
    )
    base_title: str = Field(
        description="The base title of the album to exclude from the results.",
        example=Defaults.API_ALBUMNAME,
    )
    artisthash: str = Field(
        description="The artist hash",
        example=Defaults.API_ARTISTHASH,
    )

@api.post("/album/versions", summary="Get other versions")
def get_album_versions(body: GetAlbumVersionsBody):
    """
    Returns other versions of the given album.
    """
    og_album_title = body.og_album_title
    base_title = body.base_title
    artisthash = body.artisthash

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

class GetSimilarAlbumsQuery(BaseModel):
    artisthash: str = Field(
        description="The artist hash",
        example=Defaults.API_ARTISTHASH,
    )
    limit: int = Field(
        description="The maximum number of albums to return",
        example=Defaults.API_CARD_LIMIT,
        default=Defaults.API_CARD_LIMIT,
    )

@api.get("/album/similar", summary="Get similar albums")
def get_similar_albums(query: GetSimilarAlbumsQuery):
    """
    Returns similar albums to the given album.
    """
    artisthash = query.artisthash
    limit = query.limit

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
