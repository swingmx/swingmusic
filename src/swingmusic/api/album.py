"""
Contains all the album routes.
"""

import random
from dataclasses import asdict

from flask_openapi3 import Tag
from pydantic import BaseModel, Field
from flask_openapi3 import APIBlueprint
from swingmusic.api.apischemas import (
    AlbumHashSchema,
    AlbumLimitSchema,
    ArtistHashSchema,
)

from swingmusic.config import UserConfig
from swingmusic.db.userdata import SimilarArtistTable
from swingmusic.models.album import Album
from swingmusic.premium import CloudError, LicenseError, classical_available
from swingmusic.store.albums import AlbumStore
from swingmusic.store.artists import ArtistStore
from swingmusic.store.tracks import TrackStore
from swingmusic.utils.hashing import create_hash
from swingmusic.lib.albumslib import sort_by_track_no
from swingmusic.serializers.album import serialize_for_card_many
from swingmusic.serializers.track import serialize_tracks
from swingmusic.utils.stats import get_track_group_stats


bp_tag = Tag(name="Album", description="Single album")
api = APIBlueprint("album", __name__, url_prefix="/album", abp_tags=[bp_tag])


class GetAlbumVersionsBody(BaseModel):
    og_album_title: str = Field(
        description="The original album title (album.og_title)",
    )

    albumhash: str = Field(
        description="The album hash of the album to exclude from the results.",
    )


class GetMoreFromArtistsBody(AlbumLimitSchema):
    albumartists: list = Field(
        description="The artist hashes to get more albums from",
    )

    base_title: str = Field(
        description="The base title of the album to exclude from the results.",
    )


class GetAlbumInfoBody(AlbumHashSchema, AlbumLimitSchema):
    classical_view: bool = Field(
        description="Whether to return the album info in classical view.",
        default=False,
    )


# NOTE: Don't use "/" as it will cause redirects (failure)
@api.post("")
def get_album_tracks_and_info(body: GetAlbumInfoBody):
    """
    Get album and tracks

    Returns album info and tracks for the given albumhash.
    """
    albumhash = body.albumhash
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

    more_from_data = GetMoreFromArtistsBody(
        albumartists=[a["artisthash"] for a in album.albumartists],
        albumlimit=body.limit,
        base_title=album.base_title,
    )
    other_versions_data = GetAlbumVersionsBody(
        albumhash=albumhash,
        og_album_title=album.og_title,
    )

    more_from_albums = get_more_from_artist(more_from_data)
    other_versions = get_album_versions(other_versions_data)

    response = {
        "stats": get_track_group_stats(tracks, is_album=True),
        "info": {
            **{key: value for key, value in asdict(album).items() if not key.startswith("_")},
            "is_favorite": album.is_favorite,
        },
        "extra": {
            # INFO: track_total is the sum of a set of track_total values from each track
            # ASSUMPTIONS
            # 1. All the tracks have the correct track totals
            # 2. Tracks with the same track total are from the same disc
            "track_total": track_total,
            "avg_bitrate": avg_bitrate,
        },
        "copyright": tracks[0].copyright,
        "more_from": more_from_albums,
        "other_versions": other_versions,
    }

    if (
        body.classical_view
        and album.is_classical
        and classical_available()
    ):
        try:
            from swingmusic.premium.classical.serializers import album_performers, serialize_album_works

            response["works"] = serialize_album_works(sort_by_track_no(tracks))
            response.update(album_performers(response["works"]))
            response["tracks"] = []
            return response
        except (LicenseError, CloudError, ImportError) as e:
            print("error serializing album works", e)

    response["tracks"] = serialize_tracks(tracks, remove_disc=False)
    return response


class GetAlbumTracksQuery(BaseModel):
    classical_view: bool = Field(
        description="Whether to return the tracks grouped as classical works.",
        default=False,
    )


@api.get("/<albumhash>/tracks")
def get_album_tracks(path: AlbumHashSchema, query: GetAlbumTracksQuery):
    """
    Get album tracks

    Returns all the tracks in the given album, sorted by disc and track number.
    NOTE: No album info is returned.
    """
    tracks = AlbumStore.get_album_tracks(path.albumhash)
    tracks = sort_by_track_no(tracks)

    albumentry = AlbumStore.albummap.get(path.albumhash)
    is_classical = albumentry is not None and albumentry.album.is_classical

    if (
        query.classical_view
        and is_classical
        and classical_available()
    ):
        try:
            from swingmusic.premium.classical.serializers import serialize_album_works

            return serialize_album_works(tracks, album_view=False)
        except (LicenseError, CloudError, ImportError) as e:
            print("error serializing album works", e)
            return []

    return serialize_tracks(tracks)


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
            and artisthash in a.artisthashes
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

    del similar_artists

    artists = ArtistStore.get_artists_by_hashes(artisthashes)
    albums = AlbumStore.get_albums_by_artisthashes([a.artisthash for a in artists])
    sample = random.sample(albums, min(len(albums), limit))

    return serialize_for_card_many(sample[:limit])
