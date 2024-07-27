"""
Contains all the album routes.
"""

from pprint import pprint
import random

from pydantic import BaseModel, Field
from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from app.api.apischemas import AlbumHashSchema, AlbumLimitSchema, ArtistHashSchema

from app.config import UserConfig
from app.db.userdata import SimilarArtistTable
from app.models.album import Album
from app.settings import Defaults
from app.store.albums import AlbumStore
from app.store.artists import ArtistStore
from app.store.tracks import TrackStore
from app.utils.hashing import create_hash
from app.lib.albumslib import sort_by_track_no
from app.serializers.album import serialize_for_card_many
from app.serializers.track import serialize_tracks
from app.db.sqlite.favorite import SQLiteFavoriteMethods as favdb

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
    # album = AlbumDb.get_album_by_albumhash(albumhash)
    albumentry = AlbumStore.albummap.get(albumhash)

    if albumentry is None:
        return {"error": "Album not found"}, 404

    album = albumentry.album
    tracks = TrackStore.get_tracks_by_trackhashes(albumentry.trackhashes)
    album.trackcount = len(tracks)
    album.duration = sum(t.duration for t in tracks)
    album.check_type(
        tracks=tracks, singleTrackAsSingle=UserConfig().showAlbumsAsSingles
    )

    track_total = sum({int(t.extra.get("track_total", 1) or 1) for t in tracks})
    avg_bitrate = sum(t.bitrate for t in tracks) // (len(tracks) or 1)

    album.fav_userids = [1]
    pprint(album)

    return {
        "info": album,
        "extra": {
            # INFO: track_total is the sum of a set of track_total values from each track
            # ASSUMPTIONS
            # 1. All the tracks have the correct track totals
            # 2. Tracks with the same track total are from the same disc
            "track_total": track_total,
            "avg_bitrate": avg_bitrate,
        },
        "copyright": tracks[0].copyright,
        "tracks": serialize_tracks(tracks, remove_disc=False),
    }


@api.get("/<albumhash>/tracks")
def get_album_tracks(path: AlbumHashSchema):
    """
    Get album tracks

    Returns all the tracks in the given album, sorted by disc and track number.
    NOTE: No album info is returned.
    """
    tracks = AlbumStore.get_album_tracks(path.albumhash)
    tracks = sort_by_track_no(tracks)

    return serialize_tracks(tracks)


class GetMoreFromArtistsBody(AlbumLimitSchema):
    albumartists: list = Field(
        description="The artist hashes to get more albums from",
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

    all_albums: dict[str, list[Album]] = {}

    for artisthash in albumartists:
        all_albums[artisthash] = AlbumStore.get_albums_by_artisthash(artisthash)

    seen_hashes = set()

    for artisthash, albums in all_albums.items():
        albums = [
            a
            for a in albums
            # INFO: filter out albums added to other artists
            if a.albumhash not in seen_hashes
            # INFO: filter out albums with the same base title
            and create_hash(a.base_title) != create_hash(base_title)
        ]
        all_albums[artisthash] = serialize_for_card_many(
            [a for a in albums if create_hash(a.base_title) != create_hash(base_title)][
                :limit
            ]
        )
        # INFO: record albums added to other artists
        seen_hashes.update([a.albumhash for a in albums][:limit])

    return all_albums


class GetAlbumVersionsBody(BaseModel):
    og_album_title: str = Field(
        description="The original album title (album.og_title)",
        example=Defaults.API_ALBUMNAME,
    )

    albumhash: str = Field(
        description="The album hash of the album to exclude from the results.",
        example=Defaults.API_ALBUMHASH,
    )


@api.post("/other-versions")
def get_album_versions(body: GetAlbumVersionsBody):
    """
    Get other versions

    Returns other versions of the given album.
    """
    albumhash = body.albumhash

    album = AlbumStore.albummap.get(albumhash)
    if not album:
        return []
    artisthash = album.album.artisthashes[0]
    albums = AlbumStore.get_albums_by_artisthash(artisthash)

    basetitle = album.basetitle
    albums = [
        a
        for a in albums
        if a.og_title != album.album.og_title
        if a.base_title == basetitle
        and artisthash in {a["artisthash"] for a in a.albumartists}
    ]

    return serialize_for_card_many(albums)


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

    similar_artists = SimilarArtistTable.get_by_hash(artisthash)

    if similar_artists is None:
        return []

    artisthashes = similar_artists.get_artist_hash_set()
    artists = ArtistStore.get_artists_by_hashes(artisthashes)
    albums = AlbumStore.get_albums_by_artisthashes([a.artisthash for a in artists])
    sample = random.sample(albums, min(len(albums), limit))

    return serialize_for_card_many(sample[:limit])
