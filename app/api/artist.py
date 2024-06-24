"""
Contains all the artist(s) routes.
"""

from itertools import groupby
import math
import random
from datetime import datetime

from flask_jwt_extended import current_user
from flask_openapi3 import APIBlueprint, Tag
from pydantic import Field
from app.api.apischemas import (
    AlbumLimitSchema,
    ArtistHashSchema,
    ArtistLimitSchema,
    TrackLimitSchema,
)

from app.config import UserConfig
from app.db import AlbumTable, ArtistTable, TrackTable
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

    artist = ArtistTable.get_artist_by_hash(artisthash)
    print(artist)

    if artist is None:
        return {"error": "Artist not found"}, 404

    tracks = TrackTable.get_tracks_by_artisthash(artisthash)
    tcount = len(tracks)

    if artist.albumcount == 0 and tcount < 10:
        limit = tcount

    # artist.is_favorite = favdb.check_is_favorite(artisthash, FavType.artist)

    try:
        year = datetime.fromtimestamp(artist.date).year
    except ValueError:
        year = 0

    decade = None

    if year:
        decade = math.floor(year / 10) * 10
        decade = str(decade)[2:] + "s"

    if decade:
        artist.genres.insert(0, {"name": decade, "genrehash": decade})

    return {
        "artist": artist,
        "tracks": serialize_tracks(tracks[:limit]),
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

    artist = ArtistTable.get_artist_by_hash(artisthash)

    if artist is None:
        return {"error": "Artist not found"}, 404

    albums = AlbumTable.get_albums_by_artisthash(artisthash)
    tracks = TrackTable.get_tracks_by_artisthash(artisthash)

    missing_albumhashes = {
        t.albumhash for t in tracks if t.albumhash not in {a.albumhash for a in albums}
    }

    albums.extend(AlbumTable.get_albums_by_hash(missing_albumhashes))
    albumdict = {a.albumhash: a for a in albums}

    config = UserConfig()
    albumgroups = groupby(tracks, key=lambda t: t.albumhash)
    for albumhash, tracks in albumgroups:
        album = albumdict.get(albumhash)

        if album:
            album.check_type(list(tracks), config.showAlbumsAsSingles)

    # all_albums = AlbumStore.get_albums_by_artisthash(artisthash)
    # start: check for missing albums. ie. compilations and features
    # all_tracks = TrackStore.get_tracks_by_artisthash(artisthash)

    # track_albums = set(t.albumhash for t in all_tracks)
    # missing_album_hashes = track_albums.difference(set(a.albumhash for a in all_albums))

    # if len(missing_album_hashes) > 0:
    #     missing_albums = AlbumStore.get_albums_by_hashes(list(missing_album_hashes))
    #     all_albums.extend(missing_albums)

    # end check

    # def get_album_tracks(albumhash: str):
    #     tracks = [t for t in all_tracks if t.albumhash == albumhash]

    #     if len(tracks) > 0:
    #         return tracks

    #     return TrackStore.get_tracks_by_albumhash(albumhash)

    # for a in all_albums:
    #     a.check_type()

    #     album_tracks = get_album_tracks(a.albumhash)

    #     if len(album_tracks) == 0:
    #         continue

    #     a.get_date_from_tracks(album_tracks)

    #     if a.date == 0:
    #         AlbumStore.remove_album_by_hash(a.albumhash)
    #         continue

    #     a.is_single(album_tracks)

    albums = [a for a in albumdict.values()]
    all_albums = sorted(albums, key=lambda a: str(a.date), reverse=True)

    res = {
        "albums": [],
        "appearances": [],
        "compilations": [],
        "singles_and_eps": [],
    }

    for album in all_albums:
        if album.type == "single" or album.type == "ep":
            res["singles_and_eps"].append(album)
        elif album.type == "compilation":
            res["compilations"].append(album)
        elif album.albumhash in missing_albumhashes:
            res["appearances"].append(album)
        else:
            res["albums"].append(album)

    # def remove_EPs_and_singles(albums_: list[Album]):
    #     albums_ = [a for a in albums_ if not a.type == "single"]
    #     albums_ = [a for a in albums_ if not a.type == "ep"]
    #     return albums_

    # albums = filter(lambda a: artisthash in missing_albumhashes, all_albums)
    # albums = list(albums)
    # albums = remove_EPs_and_singles(albums)

    # compilations = [a for a in albums if a.is_compilation]
    # for c in compilations:
    #     albums.remove(c)

    # appearances = filter(lambda a: artisthash not in a.albumartists_hashes, all_albums)
    # appearances = list(appearances)

    # appearances = remove_EPs_and_singles(appearances)

    # artist = ArtistStore.get_artist_by_hash(artisthash)

    # if artist is None:
    #     return {"error": "Artist not found"}, 404

    if return_all:
        limit = len(all_albums)

    # loop through the res dict and serialize the albums
    for key, value in res.items():
        res[key] = serialize_for_card_many(value[:limit])

    res["artistname"] = artist.name
    return res


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
