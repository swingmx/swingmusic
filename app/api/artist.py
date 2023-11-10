"""
Contains all the artist(s) routes.
"""
import math
import random
from datetime import datetime

from flask import Blueprint, request

from app.db.sqlite.favorite import SQLiteFavoriteMethods as favdb
from app.db.sqlite.lastfm.similar_artists import SQLiteLastFMSimilarArtists as fmdb
from app.models import Album, FavType
from app.serializers.album import serialize_for_card_many
from app.serializers.track import serialize_tracks
from app.store.albums import AlbumStore
from app.store.artists import ArtistStore
from app.store.tracks import TrackStore

api = Blueprint("artist", __name__, url_prefix="/")


@api.route("/artist/<artisthash>", methods=["GET"])
def get_artist(artisthash: str):
    """
    Get artist data.
    """
    limit = request.args.get("limit")

    if limit is None:
        limit = 6

    limit = int(limit)

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


@api.route("/artist/<artisthash>/albums", methods=["GET"])
def get_artist_albums(artisthash: str):
    limit = request.args.get("limit")

    if limit is None:
        limit = 6

    return_all = request.args.get("all")

    limit = int(limit)

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


@api.route("/artist/<artisthash>/tracks", methods=["GET"])
def get_all_artist_tracks(artisthash: str):
    """
    Returns all artists by a given artist.
    """
    tracks = TrackStore.get_tracks_by_artisthash(artisthash)

    return {"tracks": serialize_tracks(tracks)}


@api.route("/artist/<artisthash>/similar", methods=["GET"])
def get_similar_artists(artisthash: str):
    """
    Returns similar artists.
    """
    limit = request.args.get("limit")

    if limit is None:
        limit = 6

    limit = int(limit)

    artist = ArtistStore.get_artist_by_hash(artisthash)

    if artist is None:
        return {"error": "Artist not found"}, 404

    result = fmdb.get_similar_artists_for(artist.artisthash)

    if result is None:
        return {"artists": []}

    similar = ArtistStore.get_artists_by_hashes(result.get_artist_hash_set())

    if len(similar) > limit:
        similar = random.sample(similar, limit)

    return {"artists": similar[:limit]}


# TODO: Rewrite this file using generators where possible
