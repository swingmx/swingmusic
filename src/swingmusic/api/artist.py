"""
Contains all the artist(s) routes.
"""

import math
import random
from datetime import datetime, timezone
from itertools import groupby
from typing import Any

from flask_openapi3 import APIBlueprint, Tag
from pydantic import BaseModel, Field
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
from swingmusic.store.artists import ArtistStore
from swingmusic.store.plays import PlayStore
from swingmusic.store.tracks import TrackStore
from swingmusic.utils.auth import get_current_userid
from swingmusic.utils.stats import get_track_group_stats, listening_rank, listening_summary

bp_tag = Tag(name="Artist", description="Single artist")
api = APIBlueprint("artist", __name__, url_prefix="/artist", abp_tags=[bp_tag])


class GetArtistAlbumsQuery(AlbumLimitSchema):
    all: bool = Field(
        description="Whether to ignore albumlimit and return all albums", default=False
    )


class ClassicalFilterQuery(BaseModel):
    category: str = Field("", description="Composer pages: only works in this category slug")
    composer: str = Field("", description="Performer pages: only works by this composer hash")


class GetArtistQuery(TrackLimitSchema, GetArtistAlbumsQuery, ClassicalFilterQuery):
    albumlimit: int = Field(7, description="The number of albums to return")


def _classical_kind(artisthash: str) -> str | None:
    """
    "composer" or "performer" when the hash is a classical person and
    classical support is on, else None.
    """
    try:
        from swingmusic.premium import classical_available

        if not classical_available():
            return None
        from swingmusic.premium.classical.serializers import person_kind

        return person_kind(artisthash)
    except Exception:  # noqa: BLE001
        return None


def _classical_filter(kind: str, query: ClassicalFilterQuery) -> str | None:
    return (query.category if kind == "composer" else query.composer) or None


# sections of a classical person's albums, in page order
CLASSICAL_SECTIONS = ("classical", "albums", "singles_and_eps", "live", "soundtracks", "compilations", "appearances")


def _classical_album_sections(page: dict, artisthash: str, limit: int | None) -> dict[str, list]:
    """
    The person's classical albums, then their other library albums by type,
    each album listed once.
    """
    seen = set(page["albumhashes"])
    groups = _album_groups(artisthash, split_types=True) or {}
    sections: dict[str, list] = {"classical": page["albums"]}
    for key in CLASSICAL_SECTIONS[1:]:
        sections[key] = serialize_for_card_many([a for a in groups.get(key, []) if a.albumhash not in seen])
    return {key: value[:limit] if limit else value for key, value in sections.items()}


@api.get("/<string:artisthash>")
def get_artist(path: ArtistHashSchema, query: GetArtistQuery):
    """
    Get artist

    Returns artist data, tracks and genres for the given artisthash.
    """
    artisthash = path.artisthash
    limit = query.limit

    kind = _classical_kind(artisthash)
    if kind is not None:
        from swingmusic.premium.classical.serializers import serialize_person

        page = serialize_person(artisthash, _classical_filter(kind, query))
        page["albums"] = _classical_album_sections(page, artisthash, query.albumlimit)
        del page["albumhashes"]
        page["listening"] = _person_listening(artisthash)
        return page

    entry = ArtistStore.artistmap.get(artisthash)

    if entry is None:
        return {"error": "Artist not found"}, 404

    tracks = TrackStore.get_tracks_by_trackhashes(entry.trackhashes)
    tracks = sort_tracks(tracks, key="playcount", reverse=True)
    tcount = len(tracks)

    artist = entry.artist
    if artist.albumcount == 0 and tcount < 10:
        limit = tcount

    try:
        year = datetime.fromtimestamp(artist.date, tz=timezone.utc).year
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
    listening = listening_summary(tracks)
    if listening is not None:
        durations = PlayStore.durations(get_current_userid(), "artist")
        rank = listening_rank(artisthash, durations)
        listening["rank"] = {**rank, "of": "artists"} if rank else None
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
    albums = get_artist_albums(path, query)

    return {
        "type": "artist",
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
        "listening": listening,
    }


def _person_listening(hash_: str) -> dict | None:
    """
    Listening totals for a composer or performer page, with its most
    played work in place of a top track.
    """
    from swingmusic.premium.classical.listening import person_rank, person_trackhashes, top_work

    tracks = TrackStore.get_tracks_by_trackhashes(person_trackhashes(hash_))
    listening = listening_summary(tracks)
    if listening is None:
        return None
    del listening["top_track"]
    listening["top_work"] = top_work(tracks)
    listening["rank"] = person_rank(hash_)
    return listening


@api.get("/<artisthash>/albums")
def get_artist_albums(path: ArtistHashSchema, query: GetArtistAlbumsQuery):
    """
    Get artist albums.
    """
    return_all = query.all
    artisthash = path.artisthash

    limit = query.limit

    kind = _classical_kind(artisthash)
    if kind is not None:
        from swingmusic.premium.classical.serializers import person_albums

        page = person_albums(artisthash)
        res = _classical_album_sections(page, artisthash, None if return_all else limit)
        res["artistname"] = page["name"]
        return res

    entry = ArtistStore.artistmap.get(artisthash)

    if entry is None:
        return {"error": "Artist not found"}, 404

    res = _album_groups(artisthash)
    all_albums = [a for group in res.values() for a in group]

    if return_all:
        limit = len(all_albums)

    # loop through the res dict and serialize the albums
    for key, value in res.items():
        res[key] = serialize_for_card_many(value[:limit])

    res["artistname"] = entry.artist.name
    return res


def _album_groups(artisthash: str, split_types: bool = False) -> dict[str, list] | None:
    """
    A library artist's albums grouped as albums, singles_and_eps,
    compilations, and appearances, newest first. With `split_types`, live
    albums and soundtracks get their own groups. None for a non-artist.
    """
    entry = ArtistStore.artistmap.get(artisthash)
    if entry is None:
        return None

    albums = AlbumStore.get_albums_by_hashes(entry.albumhashes)
    tracks = TrackStore.get_tracks_by_trackhashes(entry.trackhashes)

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
    if split_types:
        res["live"] = []
        res["soundtracks"] = []

    for album in all_albums:
        is_appearance = (
            album.albumhash in missing_albumhashes
            or artisthash not in album.artisthashes
        )

        if album.type == "single" or album.type == "ep":
            res["singles_and_eps"].append(album)
        elif is_appearance:
            res["appearances"].append(album)
        elif album.type == "compilation":
            res["compilations"].append(album)
        elif split_types and album.type == "live album":
            res["live"].append(album)
        elif split_types and album.type == "soundtrack":
            res["soundtracks"].append(album)
        else:
            res["albums"].append(album)

    return res


@api.get("/<artisthash>/tracks")
def get_all_artist_tracks(path: ArtistHashSchema):
    """
    Get artist tracks

    Returns all artists by a given artist. For a composer or performer,
    returns their repertoire as works with movements, for queueing.
    """
    if _classical_kind(path.artisthash) is not None:
        from swingmusic.premium.classical.serializers import serialize_person_tracks

        return serialize_person_tracks(path.artisthash)

    tracks = ArtistStore.get_artist_tracks(path.artisthash)
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


@api.get("/<artisthash>/works")
def get_artist_works(path: ArtistHashSchema, query: ClassicalFilterQuery):
    """
    Get every work by a composer, or recorded by a performer

    Filtered by `category` (composers) or `composer` (performers). Responds
    404 for anyone else.
    """
    kind = _classical_kind(path.artisthash)
    if kind is None:
        return {"error": "Not a composer or performer"}, 404

    from swingmusic.premium.classical.serializers import serialize_person_works

    return serialize_person_works(path.artisthash, _classical_filter(kind, query))


@api.get("/<artisthash>/similar")
def get_similar_artists(path: ArtistHashSchema, query: ArtistLimitSchema):
    """
    Get similar artists.
    """
    limit = query.limit
    result = SimilarArtistTable.get_by_hash(path.artisthash)

    if result is None:
        return []

    similar = ArtistStore.get_artists_by_hashes(result.get_artist_hash_set())

    if len(similar) > limit:
        similar = random.sample(similar, min(limit, len(similar)))

    return serialize_for_cards(similar[:limit])
