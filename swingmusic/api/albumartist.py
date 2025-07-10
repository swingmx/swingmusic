# swingmusic/api/albumartist.py (New file)
"""
Contains all the album artist(s) routes.
"""

import math
import random
from datetime import datetime
from itertools import groupby
from typing import Any

from flask_openapi3 import APIBlueprint, Tag
from pydantic import Field
from pydantic import BaseModel
from swingmusic.api.apischemas import (
    AlbumLimitSchema,
    ArtistHashSchema,
    ArtistLimitSchema,
    TrackLimitSchema,
)

from swingmusic.config import UserConfig
from swingmusic.db.userdata import SimilarArtistTable
from swingmusic.lib.sortlib import sort_tracks

from swingmusic.serializers.album import serialize_for_card_many
from swingmusic.serializers.artist import serialize_for_cards, serialize_for_card
from swingmusic.serializers.track import serialize_track

from swingmusic.store.albums import AlbumStore
from swingmusic.store.albumartists import AlbumArtistStore
from swingmusic.store.tracks import TrackStore
from swingmusic.utils.stats import get_track_group_stats

bp_tag = Tag(name="Album Artist", description="Single album artist")
api = APIBlueprint("albumartist", __name__, url_prefix="/albumartist", abp_tags=[bp_tag])


class GetAlbumArtistAlbumsQuery(AlbumLimitSchema):
    all: bool = Field(
        description="Whether to ignore albumlimit and return all albums", default=False
    )

class GetAlbumArtistQuery(TrackLimitSchema, GetAlbumArtistAlbumsQuery):
    albumlimit: int = Field(7, description="The number of albums to return")

class SearchAlbumArtistsQuery(BaseModel):
    query: str = Field(default="", description="Search query for album artist names")
    limit: int = Field(default=50, description="Maximum number of results to return")

@api.get("/<string:artisthash>")
def get_album_artist(path: ArtistHashSchema, query: GetAlbumArtistQuery):
    """
    Get album artist

    Returns album artist data, tracks and genres for the given artisthash.
    """
    artisthash = path.artisthash
    limit = query.limit

    entry = AlbumArtistStore.albumartistmap.get(artisthash)

    if entry is None:
        return {"error": "Album artist not found"}, 404

    tracks = AlbumArtistStore.get_album_artist_tracks(artisthash)
    tracks = sort_tracks(tracks, key="playcount", reverse=True)
    tcount = len(tracks)

    artist = entry.artist
    if artist.albumcount == 0 and tcount < 10:
        limit = tcount

    try:
        year = datetime.fromtimestamp(artist.date).year
    except ValueError:
        year = 0

    genres = [*artist.genres]
    decade = None

    if year:
        decade = math.floor(year / 10) * 10
        decade = str(decade)[2:] + "s"

    if decade:
        genres.insert(0, {"name": decade, "genrehash": decade})

    stats = get_track_group_stats(tracks)
    duration = sum(t.duration for t in tracks) if tracks else 0
    tracks = tracks[:limit] if (limit and limit != -1) else tracks
    tracks = [
        {
            **serialize_track(t),
            "help_text": (
                "unplayed"
                if t.playcount == 0
                else f"{t.playcount} play{'' if t.playcount == 1 else 's'}"
            ),
        }
        for t in tracks
    ]

    query.limit = query.albumlimit
    albums = get_album_artist_albums(path, query)

    return {
        "artist": {
            **serialize_for_card(artist),
            "duration": duration,
            "trackcount": tcount,
            "albumcount": artist.albumcount,
            "genres": genres,
            "is_favorite": artist.is_favorite,
        },
        "tracks": tracks,
        "albums": albums,
        "stats": stats,
    }


@api.get("/<artisthash>/albums")
def get_album_artist_albums(path: ArtistHashSchema, query: GetAlbumArtistAlbumsQuery):
    """
    Get album artist albums.
    """
    return_all = query.all
    artisthash = path.artisthash
    limit = query.limit

    entry = AlbumArtistStore.albumartistmap.get(artisthash)

    if entry is None:
        return {"error": "Album artist not found"}, 404

    albums = AlbumStore.get_albums_by_hashes(entry.albumhashes)
    tracks = TrackStore.get_tracks_by_trackhashes(entry.trackhashes)

    # Get any missing albums from tracks
    missing_albumhashes = {
        t.albumhash for t in tracks if t.albumhash not in {a.albumhash for a in albums}
    }

    albums.extend(AlbumStore.get_albums_by_hashes(missing_albumhashes))
    albumdict = {a.albumhash: a for a in albums}

    config = UserConfig()
    albumgroups = groupby(tracks, key=lambda t: t.albumhash)
    for albumhash, tracks in albumgroups:
        album = albumdict.get(albumhash)

        if album:
            album.check_type(list(tracks), config.showAlbumsAsSingles)

    albums = [a for a in albumdict.values()]
    all_albums = sorted(albums, key=lambda a: a.date, reverse=True)

    res: dict[str, Any] = {
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
        elif (
            album.albumhash in missing_albumhashes
            or artisthash not in album.artisthashes
        ):
            res["appearances"].append(album)
        else:
            res["albums"].append(album)

    if return_all:
        limit = len(all_albums)

    # loop through the res dict and serialize the albums
    for key, value in res.items():
        res[key] = serialize_for_card_many(value[:limit])

    res["artistname"] = entry.artist.name
    return res


@api.get("/<artisthash>/tracks")
def get_all_album_artist_tracks(path: ArtistHashSchema):
    """
    Get album artist tracks

    Returns all tracks by a given album artist.
    """
    tracks = AlbumArtistStore.get_album_artist_tracks(path.artisthash)
    tracks = sort_tracks(tracks, key="playcount", reverse=True)
    tracks = [
        {
            **serialize_track(t),
            "help_text": (
                "unplayed"
                if t.playcount == 0
                else f"{t.playcount} play{'' if t.playcount == 1 else 's'}"
            ),
        }
        for t in tracks
    ]

    return tracks


@api.get("/<artisthash>/similar")
def get_similar_album_artists(path: ArtistHashSchema, query: ArtistLimitSchema):
    """
    Get similar album artists.
    """
    limit = query.limit
    result = SimilarArtistTable.get_by_hash(path.artisthash)

    if result is None:
        return []

    # Get similar artists from both regular artists and album artists
    similar_hashes = result.get_artist_hash_set()
    similar = AlbumArtistStore.get_artists_by_hashes(similar_hashes)

    if len(similar) > limit:
        similar = random.sample(similar, min(limit, len(similar)))

    return serialize_for_cards(similar[:limit])

@api.get("/search")
def search_album_artists(query: SearchAlbumArtistsQuery):
    """
    Search album artists by name.
    """
    if not query.query:
        return []
    
    results = AlbumArtistStore.search_album_artists(query.query, query.limit)
    return serialize_for_cards(results)

@api.get("/stats")
def get_album_artist_stats():
    """
    Get album artist statistics.
    """
    return AlbumArtistStore.get_stats()