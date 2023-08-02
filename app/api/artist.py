"""
Contains all the artist(s) routes.
"""
from collections import deque
import random

from flask import Blueprint, request

from app.db.sqlite.favorite import SQLiteFavoriteMethods as favdb
from app.db.sqlite.lastfm.similar_artists import SQLiteLastFMSimilarArtists as fmdb

from app.models import Album, FavType, Track
from app.serializers.album import serialize_for_card_many
from app.serializers.track import serialize_tracks
from app.utils.remove_duplicates import remove_duplicates

from app.store.albums import AlbumStore
from app.store.tracks import TrackStore
from app.store.artists import ArtistStore

api = Blueprint("artist", __name__, url_prefix="/")


class CacheEntry:
    """
    The cache entry class for the artists cache.
    """

    def __init__(
        self, artisthash: str, albumhashes: set[str], tracks: list[Track]
    ) -> None:
        self.albums: list[Album] = []
        self.tracks: list[Track] = []

        self.artisthash: str = artisthash
        self.albumhashes: set[str] = albumhashes

        if len(tracks) > 0:
            self.tracks: list[Track] = tracks

        self.type_checked = False
        self.albums_fetched = False


class ArtistsCache:
    """
    Holds artist page cache.
    """

    artists: deque[CacheEntry] = deque(maxlen=1)
    # THE ABOVE IS SET TO MAXLEN=1 TO AVOID A BUG THAT I WAS TOO LAZY TO INVESTIGATE
    # ARTIST TRACKS SOMEHOW DISAPPEARED FOR SOME REASON I COULDN'T UNDERSTAND. BY
    # DISAPPEARING I MEAN AN ARTIST YOU ARE SURE HAS 150 TRACKS ONLY SHOWING LIKE 3 IN
    # THE ARTIST PAGE. 🤷🏿 (TODO: MAYBE FIX THIS BUG?)

    @classmethod
    def get_albums_by_artisthash(cls, artisthash: str) -> tuple[list[Album], int]:
        """
        Returns the cached albums for the given artisthash.
        """
        for index, albums in enumerate(cls.artists):
            if albums.artisthash == artisthash:
                return albums.albums, index

        return [], -1

    @classmethod
    def albums_cached(cls, artisthash: str) -> bool:
        """
        Returns True if the artist is in the cache.
        """
        for entry in cls.artists:
            if entry.artisthash == artisthash and len(entry.albums) > 0:
                return True

        return False

    @classmethod
    def albums_fetched(cls, artisthash: str):
        """
        Checks if the albums have been fetched for the given artisthash.
        """
        for entry in cls.artists:
            if entry.artisthash == artisthash:
                return entry.albums_fetched

    @classmethod
    def tracks_cached(cls, artisthash: str) -> bool:
        """
        Checks if the tracks have been cached for the given artisthash.
        """
        for entry in cls.artists:
            if entry.artisthash == artisthash and len(entry.tracks) > 0:
                return True

        return False

    @classmethod
    def add_entry(cls, artisthash: str, albumhashes: set[str], tracks: list[Track]):
        """
        Adds a new entry to the cache.
        """
        cls.artists.append(CacheEntry(artisthash, albumhashes, tracks))

    @classmethod
    def get_tracks(cls, artisthash: str):
        """
        Returns the cached tracks for the given artisthash.
        """
        entry = [a for a in cls.artists if a.artisthash == artisthash][0]
        return entry.tracks

    @classmethod
    def get_albums(cls, artisthash: str):
        """
        Returns the cached albums for the given artisthash.
        """
        entry = [a for a in cls.artists if a.artisthash == artisthash][0]

        albums = [AlbumStore.get_album_by_hash(h) for h in entry.albumhashes]
        entry.albums = [album for album in albums if album is not None]

        store_albums = AlbumStore.get_albums_by_artisthash(artisthash)

        all_albums_hash = "-".join([a.albumhash for a in entry.albums])

        for album in store_albums:
            if album.albumhash not in all_albums_hash:
                entry.albums.append(album)

        entry.albums_fetched = True

    @classmethod
    def process_album_type(cls, artisthash: str):
        """
        Checks the cached albums type for the given artisthash.
        """
        entry = [a for a in cls.artists if a.artisthash == artisthash][0]

        for album in entry.albums:
            album.check_type()

            album_tracks = TrackStore.get_tracks_by_albumhash(album.albumhash)
            album_tracks = remove_duplicates(album_tracks)

            album.get_date_from_tracks(album_tracks)

            if album.date == 0:
                AlbumStore.remove_album_by_hash(album.albumhash)
                continue

            album.check_is_single(album_tracks)

        entry.type_checked = True
        entry.albums.sort(key=lambda a: a.date, reverse=True)


def add_albums_to_cache(artisthash: str):
    """
    Fetches albums and adds them to the cache.
    """
    tracks = TrackStore.get_tracks_by_artist(artisthash)

    if len(tracks) == 0:
        return False

    albumhashes = set(t.albumhash for t in tracks)
    ArtistsCache.add_entry(artisthash, albumhashes, [])

    return True


# =======================================================
# ===================== ROUTES ==========================
# =======================================================


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

    tracks_cached = ArtistsCache.tracks_cached(artisthash)

    if tracks_cached:
        tracks = ArtistsCache.get_tracks(artisthash)
    else:
        tracks = TrackStore.get_tracks_by_artist(artisthash)
        albumhashes = set(t.albumhash for t in tracks)
        hashes_from_albums = set(
            a.albumhash for a in AlbumStore.get_albums_by_artisthash(artisthash)
        )

        albumhashes = albumhashes.union(hashes_from_albums)
        ArtistsCache.add_entry(artisthash, albumhashes, tracks)

    tcount = len(tracks)
    acount = AlbumStore.count_albums_by_artisthash(artisthash)

    if acount == 0 and tcount < 10:
        limit = tcount

    artist.set_trackcount(tcount)
    artist.set_albumcount(acount)
    artist.set_duration(sum(t.duration for t in tracks))

    artist.is_favorite = favdb.check_is_favorite(artisthash, FavType.artist)

    return {"artist": artist, "tracks": serialize_tracks(tracks[:limit])}


@api.route("/artist/<artisthash>/albums", methods=["GET"])
def get_artist_albums(artisthash: str):
    limit = request.args.get("limit")

    if limit is None:
        limit = 6

    return_all = request.args.get("all")

    limit = int(limit)

    is_cached = ArtistsCache.albums_cached(artisthash)

    if not is_cached:
        add_albums_to_cache(artisthash)

    albums_fetched = ArtistsCache.albums_fetched(artisthash)

    if not albums_fetched:
        ArtistsCache.get_albums(artisthash)

    all_albums, index = ArtistsCache.get_albums_by_artisthash(artisthash)

    if not ArtistsCache.artists[index].type_checked:
        ArtistsCache.process_album_type(artisthash)

    singles = [a for a in all_albums if a.is_single]
    eps = [a for a in all_albums if a.is_EP]

    def remove_EPs_and_singles(albums_: list[Album]):
        albums_ = [a for a in albums_ if not a.is_EP]
        albums_ = [a for a in albums_ if not a.is_single]
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

    if return_all is not None:
        limit = len(all_albums)

    return {
        "artistname": artist.name,
        "albums": serialize_for_card_many(albums[:limit]),
        "singles": serialize_for_card_many(singles[:limit]),
        "eps": serialize_for_card_many(eps[:limit]),
        "appearances": serialize_for_card_many(appearances[:limit]),
        "compilations": serialize_for_card_many(compilations[:limit]),
    }


@api.route("/artist/<artisthash>/tracks", methods=["GET"])
def get_all_artist_tracks(artisthash: str):
    """
    Returns all artists by a given artist.
    """
    tracks = TrackStore.get_tracks_by_artist(artisthash)

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

    # result = LastFMStore.get_similar_artists_for(artist.artisthash)
    result = fmdb.get_similar_artists_for(artist.artisthash)

    if result is None:
        return {"artists": []}

    similar = ArtistStore.get_artists_by_hashes(result.get_artist_hash_set())

    if len(similar) > limit:
        similar = random.sample(similar, limit)

    return {"artists": similar[:limit]}

# TODO: Rewrite this file using generators where possible