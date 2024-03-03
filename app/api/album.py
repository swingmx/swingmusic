"""
Contains all the album routes.
"""

import random

from pydantic import Field
from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from app.api.apischemas import AlbumHashSchema, AlbumLimitSchema, ArtistHashSchema

from app.settings import Defaults
from app.models import FavType, Track
from app.store.albums import AlbumStore
from app.store.tracks import TrackStore
from app.utils.hashing import create_hash
from app.lib.albumslib import sort_by_track_no
from app.serializers.album import serialize_for_card
from app.serializers.track import serialize_track
from app.db.sqlite.albumcolors import SQLiteAlbumMethods as adb
from app.db.sqlite.favorite import SQLiteFavoriteMethods as favdb
from app.db.sqlite.lastfm.similar_artists import SQLiteLastFMSimilarArtists as lastfmdb

get_albums_by_albumartist = adb.get_albums_by_albumartist
check_is_fav = favdb.check_is_favorite

bp_tag = Tag(name="Album", description="Single album")
api = APIBlueprint("album", __name__, url_prefix="/album", abp_tags=[bp_tag])


# NOTE: Don't use "/" as it will cause redirects (failure)
@api.post("")
def get_album_tracks_and_info(body: AlbumHashSchema):
    """
    Get album and tracks

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


@api.get("/<albumhash>/tracks")
def get_album_tracks(path: AlbumHashSchema):
    """
    Get album tracks

    Returns all the tracks in the given album, sorted by disc and track number.
    NOTE: No album info is returned.
    """
    tracks = TrackStore.get_tracks_by_albumhash(path.albumhash)
    tracks = sort_by_track_no(tracks)

    return tracks


class GetMoreFromArtistsBody(AlbumLimitSchema):
    albumartists: str = Field(
        description="The artist hashes to get more albums from",
        example=Defaults.API_ARTISTHASH,
    )

    base_title: str = Field(
        description="The base title of the album to exclude from the results.",
        example=Defaults.API_ALBUMNAME,
        default=None,
    )


@api.post("/from-artist")
def get_more_from_artist(body: GetMoreFromArtistsBody):
    """
    Get more from artist

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

    return albums


class GetAlbumVersionsBody(ArtistHashSchema):
    og_album_title: str = Field(
        description="The original album title (album.og_title)",
        example=Defaults.API_ALBUMNAME,
    )
    base_title: str = Field(
        description="The base title of the album to exclude from the results.",
        example=Defaults.API_ALBUMNAME,
    )


@api.post("/other-versions")
def get_album_versions(body: GetAlbumVersionsBody):
    """
    Get other versions

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

    return albums


class GetSimilarAlbumsQuery(ArtistHashSchema, AlbumLimitSchema):
    pass


@api.get("/similar")
def get_similar_albums(query: GetSimilarAlbumsQuery):
    """
    Get similar albums

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

    return [serialize_for_card(a) for a in albums[:limit]]
