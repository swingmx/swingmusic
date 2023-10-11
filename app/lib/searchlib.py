"""
This library contains all the functions related to the search functionality.
"""
from typing import Any, Generator, List, TypeVar

from rapidfuzz import process, utils
from unidecode import unidecode

from app import models
from app.db.sqlite.favorite import SQLiteFavoriteMethods as favdb
from app.models.enums import FavType
from app.models.track import Track
from app.serializers.album import serialize_for_card as serialize_album
from app.serializers.album import serialize_for_card_many as serialize_albums
from app.serializers.artist import serialize_for_cards
from app.serializers.track import serialize_track, serialize_tracks
from app.store.albums import AlbumStore
from app.store.artists import ArtistStore
from app.store.tracks import TrackStore
from app.utils.remove_duplicates import remove_duplicates

# ratio = fuzz.ratio
# wratio = fuzz.WRatio


class Cutoff:
    """
    Holds all the default cutoff values.
    """

    tracks: int = 75
    albums: int = 75
    artists: int = 75
    playlists: int = 75


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
        self.tracks = TrackStore.tracks

    def __call__(self) -> List[models.Track]:
        """
        Gets all songs with a given title.
        """

        track_titles = [unidecode(track.og_title).lower() for track in self.tracks]
        results = process.extract(
            self.query,
            track_titles,
            score_cutoff=Cutoff.tracks,
            limit=Limit.tracks,
            processor=utils.default_process,
        )

        tracks = [self.tracks[i[2]] for i in results]
        return remove_duplicates(tracks)


class SearchArtists:
    def __init__(self, query: str) -> None:
        self.query = query
        self.artists = ArtistStore.artists

    def __call__(self):
        """
        Gets all artists with a given name.
        """
        artists = [unidecode(a.name).lower() for a in self.artists]

        results = process.extract(
            self.query,
            artists,
            score_cutoff=Cutoff.artists,
            limit=Limit.artists,
            processor=utils.default_process,
        )

        return [self.artists[i[2]] for i in results]


class SearchAlbums:
    def __init__(self, query: str) -> None:
        self.query = query
        self.albums = AlbumStore.albums

    def __call__(self) -> List[models.Album]:
        """
        Gets all albums with a given title.
        """

        albums = [unidecode(a.og_title).lower() for a in self.albums]

        results = process.extract(
            self.query,
            albums,
            score_cutoff=Cutoff.albums,
            limit=Limit.albums,
            processor=utils.default_process,
        )

        return [self.albums[i[2]] for i in results]


class SearchPlaylists:
    def __init__(self, playlists: List[models.Playlist], query: str) -> None:
        self.playlists = playlists
        self.query = query

    def __call__(self) -> List[models.Playlist]:
        playlists = [p.name for p in self.playlists]
        results = process.extract(
            self.query,
            playlists,
            score_cutoff=Cutoff.playlists,
            limit=Limit.playlists,
            processor=utils.default_process,
        )

        return [self.playlists[i[2]] for i in results]


_type = models.Track | models.Album | models.Artist
_S2 = TypeVar("_S2")
_ResultType = int | float


def get_titles(items: _type):
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

        all_items.extend(ArtistStore.artists)
        all_items.extend(TrackStore.tracks)
        all_items.extend(AlbumStore.albums)

        return all_items, get_titles(all_items)

    @staticmethod
    def get_results(items: Generator[str, Any, None], query: str):
        items = list(items)

        results = process.extract(
            query=query, choices=items, score_cutoff=Cutoff.tracks, limit=1
        )

        return results

    @staticmethod
    def map_with_type(item: _type):
        """
        Map the results to their respective types.
        """
        if isinstance(item, models.Track):
            return {"type": "track", "item": item}

        if isinstance(item, models.Album):
            tracks = TrackStore.get_tracks_by_albumhash(item.albumhash)
            tracks = remove_duplicates(tracks)

            item.get_date_from_tracks(tracks)
            try:
                item.duration = sum((t.duration for t in tracks))
            except AttributeError:
                item.duration = 0

            item.check_is_single(tracks)

            if not item.is_single:
                item.check_type()

            item.is_favorite = favdb.check_is_favorite(
                item.albumhash, fav_type=FavType.album
            )

            return {"type": "album", "item": item}

        if isinstance(item, models.Artist):
            track_count = 0
            duration = 0

            for track in TrackStore.get_tracks_by_artisthash(item.artisthash):
                track_count += 1
                duration += track.duration

            album_count = AlbumStore.count_albums_by_artisthash(item.artisthash)

            item.set_trackcount(track_count)
            item.set_albumcount(album_count)
            item.set_duration(duration)

            return {"type": "artist", "item": item}

    @staticmethod
    def get_track_items(item: dict[str, _type], query: str, limit=5):
        tracks: list[Track] = []

        if item["type"] == "track":
            tracks.extend(SearchTracks(query)())

        if item["type"] == "album":
            t = TrackStore.get_tracks_by_albumhash(item["item"].albumhash)
            t.sort(key=lambda x: x.last_mod)

            # if there are less than the limit, get more tracks
            if len(t) < limit:
                remainder = limit - len(t)
                more_tracks = SearchTracks(query)()
                t.extend(more_tracks[:remainder])

            tracks.extend(t)

        if item["type"] == "artist":
            t = TrackStore.get_tracks_by_artisthash(item["item"].artisthash)

            # if there are less than the limit, get more tracks
            if len(t) < limit:
                remainder = limit - len(t)
                more_tracks = SearchTracks(query)()
                t.extend(more_tracks[:remainder])

            tracks.extend(t)

        return tracks[:limit]

    @staticmethod
    def get_album_items(item: dict[str, _type], query: str, limit=6):
        if item["type"] == "track":
            return SearchAlbums(query)()[:limit]

        if item["type"] == "album":
            return SearchAlbums(query)()[:limit]

        if item["type"] == "artist":
            albums = AlbumStore.get_albums_by_artisthash(item["item"].artisthash)

            # if there are less than the limit, get more albums
            if len(albums) < limit:
                remainder = limit - len(albums)
                more_albums = SearchAlbums(query)()
                albums.extend(more_albums[:remainder])

            return albums[:limit]

    @staticmethod
    def search(
        query: str,
        limit: int = None,
        albums_only=False,
        tracks_only=False,
        in_quotes=False,
    ):
        items, titles = TopResults.collect_all()
        results = TopResults.get_results(titles, query)

        tracks_limit = Limit.tracks if tracks_only else 4
        albums_limit = Limit.albums if albums_only else limit
        artists_limit = limit

        # map results to their respective items
        try:
            result = [items[i[2]] for i in results][0]
        except IndexError:
            if tracks_only:
                return []

            if albums_only:
                return []

            return {
                "top_result": None,
                "tracks": [],
                "artists": [],
                "albums": [],
            }

        result = TopResults.map_with_type(result)

        if in_quotes:
            top_tracks = SearchTracks(query)()[:tracks_limit]
        else:
            top_tracks = TopResults.get_track_items(result, query, limit=tracks_limit)

        top_tracks = serialize_tracks(top_tracks)

        if tracks_only:
            return top_tracks

        if in_quotes:
            albums = SearchAlbums(query)()[:albums_limit]
        else:
            albums = TopResults.get_album_items(result, query, limit=albums_limit)

        albums = serialize_albums(albums)

        if albums_only:
            return albums

        artists = SearchArtists(query)()[:artists_limit]
        artists = serialize_for_cards(artists)

        if result["type"] == "track":
            result["item"] = serialize_track(result["item"])

        if result["type"] == "album":
            result["item"] = serialize_album(result["item"])

        return {
            "top_result": result,
            "tracks": top_tracks,
            "artists": artists,
            "albums": albums,
        }
