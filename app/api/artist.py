"""
Contains all the artist(s) routes.
"""

import math
import random
from datetime import datetime

from flask_openapi3 import APIBlueprint, Tag
from pydantic import Field
from app.api.apischemas import AlbumLimitSchema, ArtistHashSchema, ArtistLimitSchema, TrackLimitSchema

from app.db.sqlite.favorite import SQLiteFavoriteMethods as favdb
from app.db.sqlite.lastfm.similar_artists import SQLiteLastFMSimilarArtists as fmdb
from app.models import Album, FavType
from app.serializers.album import serialize_for_card_many
from app.serializers.track import serialize_tracks
from app.store.albums import AlbumStore
from app.store.artists import ArtistStore
from app.store.tracks import TrackStore

bp_tag = Tag(name="Artist", description="Single artist")
api = APIBlueprint("artist", __name__, url_prefix="/artist", abp_tags=[bp_tag])


@api.get("/<string:artisthash>")
def get_artist(path: ArtistHashSchema, query: TrackLimitSchema):
    """
    Get artist

    Returns artist data, tracks and genres for the given artisthash.
    """
    artisthash = path.artisthash
    limit = query.limit

    artist = ArtistStore.get_artist_by_hash(artisthash)

    if artist is None:
        return {"error": "Artist not found"}, 404

    tracks = TrackStore.get_tracks_by_artisthash(artisthash)
    tcount = len(tracks)
    acount = AlbumStore.count_albums_by_artisthash(artisthash)

    if acount == 0 and tcount < 10:
        limit = tcount

    artist.set_trackcount(tcount)
    artist.set_albumcount(acount)
    artist.set_duration(sum(t.duration for t in tracks))

    artist.is_favorite = favdb.check_is_favorite(artisthash, FavType.artist)

    genres = set()

    for t in tracks:
        if t.genre is not None:
            genres = genres.union(t.genre)

    genres = list(genres)

    try:
        min_stamp = min(t.date for t in tracks)
        year = datetime.fromtimestamp(min_stamp).year
    except ValueError:
        year = 0

    decade = None

    if year:
        decade = math.floor(year / 10) * 10
        decade = str(decade)[2:] + "s"

    if decade:
        genres.insert(0, decade)

    return {
        "artist": artist,
        "tracks": serialize_tracks(tracks[:limit]),
        "genres": genres,
    }


class GetArtistAlbumsQuery(AlbumLimitSchema):
    all: bool = Field(
        description="Whether to ignore limit and return all albums", default=False
    )


@api.get("/<artisthash>/albums")
def get_artist_albums(path: ArtistHashSchema, query: GetArtistAlbumsQuery):
    """
    Get artist albums.
    """
    return_all = query.all
    artisthash = path.artisthash

    limit = query.limit

    all_albums = AlbumStore.get_albums_by_artisthash(artisthash)

    # start: check for missing albums. ie. compilations and features
    all_tracks = TrackStore.get_tracks_by_artisthash(artisthash)

    track_albums = set(t.albumhash for t in all_tracks)
    missing_album_hashes = track_albums.difference(set(a.albumhash for a in all_albums))

    if len(missing_album_hashes) > 0:
        missing_albums = AlbumStore.get_albums_by_hashes(list(missing_album_hashes))
        all_albums.extend(missing_albums)

    # end check

    def get_album_tracks(albumhash: str):
        tracks = [t for t in all_tracks if t.albumhash == albumhash]

        if len(tracks) > 0:
            return tracks

        return TrackStore.get_tracks_by_albumhash(albumhash)

    for a in all_albums:
        a.check_type()

        album_tracks = get_album_tracks(a.albumhash)

        if len(album_tracks) == 0:
            continue

        a.get_date_from_tracks(album_tracks)

        if a.date == 0:
            AlbumStore.remove_album_by_hash(a.albumhash)
            continue

        a.check_is_single(album_tracks)

    all_albums = sorted(all_albums, key=lambda a: str(a.date), reverse=True)

    singles = [a for a in all_albums if a.is_single]
    eps = [a for a in all_albums if a.is_EP]

    def remove_EPs_and_singles(albums_: list[Album]):
        albums_ = [a for a in albums_ if not a.is_single]
        albums_ = [a for a in albums_ if not a.is_EP]
        return albums_

    albums = filter(lambda a: artisthash in a.albumartists_hashes, all_albums)
    albums = list(albums)
    albums = remove_EPs_and_singles(albums)

    compilations = [a for a in albums if a.is_compilation]
    for c in compilations:
        albums.remove(c)

    appearances = filter(lambda a: artisthash not in a.albumartists_hashes, all_albums)
    appearances = list(appearances)

    appearances = remove_EPs_and_singles(appearances)

    artist = ArtistStore.get_artist_by_hash(artisthash)

    if artist is None:
        return {"error": "Artist not found"}, 404

    if return_all is not None and return_all == "true":
        limit = len(all_albums)

    singles_and_eps = singles + eps

    return {
        "artistname": artist.name,
        "albums": serialize_for_card_many(albums[:limit]),
        "singles_and_eps": serialize_for_card_many(singles_and_eps[:limit]),
        "appearances": serialize_for_card_many(appearances[:limit]),
        "compilations": serialize_for_card_many(compilations[:limit]),
    }


@api.get("/<artisthash>/tracks")
def get_all_artist_tracks(path: ArtistHashSchema):
    """
    Get artist tracks

    Returns all artists by a given artist.
    """
    tracks = TrackStore.get_tracks_by_artisthash(path.artisthash)

    return serialize_tracks(tracks)


@api.get("/<artisthash>/similar")
def get_similar_artists(path: ArtistHashSchema, query: ArtistLimitSchema):
    """
    Get similar artists.
    """
    limit = query.limit

    artist = ArtistStore.get_artist_by_hash(path.artisthash)

    if artist is None:
        return {"error": "Artist not found"}, 404

    result = fmdb.get_similar_artists_for(artist.artisthash)

    if result is None:
        return {"artists": []}

    similar = ArtistStore.get_artists_by_hashes(result.get_artist_hash_set())

    if len(similar) > limit:
        similar = random.sample(similar, limit)

    return similar[:limit]


# TODO: Rewrite this file using generators where possible
