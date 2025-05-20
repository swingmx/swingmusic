"""
This library contains all the functions related to the search functionality.
"""

from typing import Any, Generator, List, TypeVar

from rapidfuzz import process, utils, fuzz
from unidecode import unidecode

from swingmusic import models
from swingmusic.config import UserConfig

# from app.db.libdata import AlbumTable, ArtistTable, TrackTable

# from app.db.sqlite.favorite import SQLiteFavoriteMethods as favdb
from swingmusic.models.album import Album
from swingmusic.models.artist import Artist
from swingmusic.models.enums import FavType
from swingmusic.models.playlist import Playlist
from swingmusic.models.track import Track
from swingmusic.serializers.album import serialize_for_card as serialize_album
from swingmusic.serializers.album import serialize_for_card_many as serialize_albums
from swingmusic.serializers.artist import serialize_for_card, serialize_for_cards
from swingmusic.serializers.track import serialize_track, serialize_tracks

from swingmusic.store.albums import AlbumStore
from swingmusic.store.artists import ArtistStore
from swingmusic.store.tracks import TrackStore

from swingmusic.utils.remove_duplicates import remove_duplicates

# ratio = fuzz.ratio
# wratio = fuzz.WRatio


class Cutoff:
    """
    Holds all the default cutoff values.
    """

    tracks: int = 50
    albums: int = 50
    artists: int = 50
    playlists: int = 50


class Limit:
    """
    Holds all the default limit values.
    """

    tracks: int = 150
    albums: int = 150
    artists: int = 150
    playlists: int = 150


class SearchTracks:
    def __init__(self, query: str) -> None:
        self.query = query
        self.tracks = TrackStore.get_flat_list()

    def __call__(self, limit: int = Limit.tracks) -> List[models.Track]:
        """
        Gets all songs with a given title.
        """

        track_titles = [unidecode(track.title).lower() for track in self.tracks]
        results = process.extract(
            self.query,
            track_titles,
            score_cutoff=Cutoff.tracks,
            limit=limit,
            processor=utils.default_process,
            scorer=fuzz.WRatio,
        )

        tracks: list[Track] = []

        for item in results:
            track = self.tracks[item[2]]
            track._score = item[1]
            tracks.append(track)

        return remove_duplicates(tracks)


class SearchArtists:
    def __init__(self, query: str) -> None:
        self.query = query
        self.artists = ArtistStore.get_flat_list()

    def __call__(self, limit: int = Limit.artists):
        """
        Gets all artists with a given name.
        """
        choices = [unidecode(a.name).lower() for a in self.artists]

        results = process.extract(
            self.query,
            choices,
            score_cutoff=Cutoff.artists,
            limit=limit,
            processor=utils.default_process,
            scorer=fuzz.WRatio,
        )

        artists: list[Artist] = []

        for item in results:
            artist = self.artists[item[2]]
            artist._score = item[1]
            artists.append(artist)

        return artists


class SearchAlbums:
    def __init__(self, query: str) -> None:
        self.query = query
        self.albums = AlbumStore.get_flat_list()

    def __call__(self, limit: int = Limit.albums):
        """
        Gets all albums with a given title.
        """

        choices = [unidecode(a.title).lower() for a in self.albums]

        results = process.extract(
            self.query,
            choices,
            score_cutoff=Cutoff.albums,
            limit=limit,
            processor=utils.default_process,
            scorer=fuzz.token_sort_ratio,
        )

        albums: list[Album] = []

        for item in results:
            album = self.albums[item[2]]
            album._score = item[1]
            albums.append(album)

        return albums


class SearchPlaylists:
    def __init__(self, playlists: List[models.Playlist], query: str) -> None:
        self.playlists = playlists
        self.query = query

    def __call__(self, limit: int = Limit.playlists):
        choices = [p.name for p in self.playlists]
        results = process.extract(
            self.query,
            choices,
            score_cutoff=Cutoff.playlists,
            limit=limit,
            processor=utils.default_process,
            scorer=fuzz.WRatio,
        )

        playlists: list[Playlist] = []

        for item in results:
            playlist = self.playlists[item[2]]
            playlist._score = item[1]
            playlists.append(playlist)

        return playlists


_type = models.Track | models.Album | models.Artist


def get_titles(items: list[_type]):
    for item in items:
        if isinstance(item, models.Track):
            text = item.og_title
        elif isinstance(item, models.Album):
            text = item.title
        elif isinstance(item, models.Artist):
            text = item.name
        else:
            text = None

        yield text


class TopResults:
    """
    Joins all tracks, albums and artists
    then fuzzy searches them as a single unit.
    """

    @staticmethod
    def collect_all():
        all_items: list[_type] = []

        all_items.extend(ArtistStore.get_flat_list())
        all_items.extend(TrackStore.get_flat_list())
        all_items.extend(AlbumStore.get_flat_list())

        return all_items, get_titles(all_items)

    @staticmethod
    def get_track_items(item: Track | Album | Artist, limit=5):
        tracks: list[Track] = []

        # INFO: If the item is a track, return empty list
        # to be filled by the results from the top search
        if isinstance(item, Track):
            return tracks

        # INFO: If the item is an album, get the tracks from the album
        if isinstance(item, Album):
            tracks = TrackStore.get_tracks_by_albumhash(item.albumhash)[:limit]
            tracks.sort(key=lambda x: x.playduration, reverse=True)
            return tracks

        # INFO: If the item is an artist, get the tracks from the artist
        if isinstance(item, Artist):
            tracks = TrackStore.get_tracks_by_artisthash(item.artisthash)[:limit]
            tracks.sort(key=lambda x: x.playduration, reverse=True)

        return tracks

    @staticmethod
    def get_album_items(item: Track | Album | Artist, limit=6):
        albums: list[Album] = []

        # INFO: If the item is a track or album, search for albums
        if isinstance(item, Track) or isinstance(item, Album):
            return albums

        # INFO: If the item is an artist, get the albums from the artist
        if isinstance(item, Artist):
            albums = AlbumStore.get_albums_by_artisthash(item.artisthash)[:limit]

        return albums

    @staticmethod
    def search(
        query: str,
        limit: int = None,
        albums_only=False,
        tracks_only=False,
    ):
        tracks_limit = Limit.tracks if tracks_only else 4
        albums_limit = Limit.albums if albums_only else limit
        artists_limit = limit

        # INFO: Individually search all stores as each type has a different scorer
        tracks = SearchTracks(query)(limit=tracks_limit) if not albums_only else []
        albums = SearchAlbums(query)(limit=albums_limit)
        artists = SearchArtists(query)(limit=artists_limit)

        # INFO: Combine all results and sort them by score
        all_results = artists + tracks + albums
        all_results = sorted(all_results, key=lambda x: int(x._score), reverse=True)

        # INFO: Get the top result
        top_result = all_results[0]
        top_tracks = []

        if not albums_only:
            top_tracks = TopResults.get_track_items(top_result, limit=tracks_limit)

            # INFO: If there are not enough tracks, fill with search results
            if len(top_tracks) < tracks_limit:
                found_tracks_set = {track.trackhash for track in top_tracks}

                for track in tracks:
                    if track.trackhash not in found_tracks_set:
                        top_tracks.append(track)

                    if len(top_tracks) >= tracks_limit:
                        break

            top_tracks = serialize_tracks(top_tracks)

            if tracks_only:
                return top_tracks

        top_albums = TopResults.get_album_items(top_result, limit=albums_limit)

        # INFO: If there are not enough albums, fill with search results
        if len(top_albums) < albums_limit:
            found_albums_set = {album.albumhash for album in top_albums}

            for album in albums:
                if album.albumhash not in found_albums_set:
                    top_albums.append(album)

                    if len(top_albums) >= albums_limit:
                        break

        top_albums = serialize_albums(top_albums)

        if albums_only:
            return top_albums

        artists = serialize_for_cards(artists)

        if isinstance(top_result, Track):
            top_result = serialize_track(top_result)
            top_result["type"] = "track"

        if isinstance(top_result, Album):
            top_result = serialize_album(top_result)
            top_result["type"] = "album"

        if isinstance(top_result, Artist):
            top_result = serialize_for_card(
                top_result, include={"albumcount", "trackcount"}
            )
            top_result["type"] = "artist"

        return {
            "top_result": top_result,
            "tracks": top_tracks,
            "artists": artists,
            "albums": top_albums,
        }
