"""
Contains all the artist(s) routes.
"""

import math
import random
from datetime import datetime
from itertools import groupby

from flask_openapi3 import APIBlueprint, Tag
from pydantic import Field
from app.api.apischemas import (
    AlbumLimitSchema,
    ArtistHashSchema,
    ArtistLimitSchema,
    TrackLimitSchema,
)

from app.config import UserConfig
from app.db.libdata import ArtistTable
from app.db.libdata import AlbumTable, TrackTable
from app.db.userdata import SimilarArtistTable

from app.serializers.album import serialize_for_card_many
from app.serializers.artist import serialize_for_cards
from app.serializers.track import serialize_tracks

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
    if artist is None:
        return {"error": "Artist not found"}, 404

    tracks = TrackTable.get_tracks_by_artisthash(artisthash)
    tcount = len(tracks)

    if artist.albumcount == 0 and tcount < 10:
        limit = tcount

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

    albums.extend(AlbumTable.get_albums_by_albumhashes(missing_albumhashes))
    albumdict = {a.albumhash: a for a in albums}

    config = UserConfig()
    albumgroups = groupby(tracks, key=lambda t: t.albumhash)
    for albumhash, tracks in albumgroups:
        album = albumdict.get(albumhash)

        if album:
            album.check_type(list(tracks), config.showAlbumsAsSingles)

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
    # tracks = TrackStore.get_tracks_by_artisthash(path.artisthash)
    tracks = TrackTable.get_tracks_by_artisthash(path.artisthash)
    return serialize_tracks(tracks)


@api.get("/<artisthash>/similar")
def get_similar_artists(path: ArtistHashSchema, query: ArtistLimitSchema):
    """
    Get similar artists.
    """
    limit = query.limit
    result = SimilarArtistTable.get_by_hash(path.artisthash)

    if result is None:
        return []

    similar = ArtistTable.get_artists_by_artisthashes(result.get_artist_hash_set())

    if len(similar) > limit:
        similar = random.sample(similar, min(limit, len(similar)))

    return serialize_for_cards(similar[:limit])
