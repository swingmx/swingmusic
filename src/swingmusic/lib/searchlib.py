"""
This library contains all the functions related to the search functionality.
"""

from rapidfuzz import process, fuzz

from swingmusic import models

from swingmusic.models.album import Album
from swingmusic.models.artist import Artist
from swingmusic.models.playlist import Playlist
from swingmusic.models.track import Track
from swingmusic.serializers.album import serialize_for_card as serialize_album
from swingmusic.serializers.album import serialize_for_card_many as serialize_albums
from swingmusic.serializers.artist import serialize_for_card, serialize_for_cards
from swingmusic.serializers.track import serialize_track, serialize_tracks

from swingmusic.store.albums import AlbumStore
from swingmusic.store.artists import ArtistStore
from swingmusic.store.tracks import TrackStore

from swingmusic.utils.parsers import normalize_search_text
from swingmusic.utils.remove_duplicates import remove_duplicates


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


def best_scores(query: str, items: list, cutoff: int) -> dict[int, float]:
    """
    Maps each matching item index to its highest score over the item's
    title and its per-artist "artist title" strings.
    """
    haystack: list[str] = []
    owners: list[int] = []

    for index, item in enumerate(items):
        haystack.append(item._search_title)
        owners.append(index)

        for text in item._search_texts:
            haystack.append(text)
            owners.append(index)

    matches = process.extract(
        query,
        haystack,
        scorer=fuzz.WRatio,
        score_cutoff=cutoff,
        limit=None,
    )

    scores: dict[int, float] = {}

    for _, score, position in matches:
        index = owners[position]

        if score > scores.get(index, 0):
            scores[index] = score

    return scores


class SearchTracks:
    def __init__(self, query: str) -> None:
        self.query = normalize_search_text(query)
        self.tracks = TrackStore.get_flat_list()

    def __call__(self, limit: int = Limit.tracks) -> list[models.Track]:
        """
        Gets tracks matching the query by title or by artist and title.
        """
        scores = best_scores(self.query, self.tracks, Cutoff.tracks)

        tracks: list[Track] = []

        for index, score in scores.items():
            track = self.tracks[index]
            track._score = score
            tracks.append(track)

        tracks.sort(key=lambda t: (t._score, t.playduration), reverse=True)
        return remove_duplicates(tracks)[:limit]


class SearchArtists:
    def __init__(self, query: str) -> None:
        self.query = normalize_search_text(query)
        self.artists = ArtistStore.get_flat_list()

    def __call__(self, limit: int = Limit.artists):
        """
        Gets all artists with a given name.
        """
        choices = [normalize_search_text(a.name) for a in self.artists]

        results = process.extract(
            self.query,
            choices,
            score_cutoff=Cutoff.artists,
            limit=limit,
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
        self.query = normalize_search_text(query)
        self.albums = AlbumStore.get_flat_list()

    def __call__(self, limit: int = Limit.albums):
        """
        Gets albums matching the query by title or by album artist and title.
        """
        scores = best_scores(self.query, self.albums, Cutoff.albums)

        albums: list[Album] = []

        for index, score in scores.items():
            album = self.albums[index]
            album._score = score
            albums.append(album)

        albums.sort(key=lambda a: (a._score, a.playduration), reverse=True)
        return albums[:limit]


class SearchPlaylists:
    def __init__(self, playlists: list[models.Playlist], query: str) -> None:
        self.playlists = playlists
        self.query = normalize_search_text(query)

    def __call__(self, limit: int = Limit.playlists):
        choices = [normalize_search_text(p.name) for p in self.playlists]
        results = process.extract(
            self.query,
            choices,
            score_cutoff=Cutoff.playlists,
            limit=limit,
            scorer=fuzz.WRatio,
        )

        playlists: list[Playlist] = []

        for item in results:
            playlist = self.playlists[item[2]]
            playlist._score = item[1]
            playlists.append(playlist)

        return playlists


class TopResults:
    """
    Searches tracks, albums and artists and builds the top results page.
    """

    TRACKS_LIMIT = 4

    @staticmethod
    def get_track_items(item: Track | Album | Artist, limit=5):
        """
        Returns the most played tracks of an album or artist.
        """
        tracks: list[Track] = []

        if isinstance(item, Album):
            tracks = TrackStore.get_tracks_by_albumhash(item.albumhash)

        if isinstance(item, Artist):
            tracks = TrackStore.get_tracks_by_artisthash(item.artisthash)

        tracks.sort(key=lambda x: x.playduration, reverse=True)
        return tracks[:limit]

    @staticmethod
    def get_album_items(item: Track | Album | Artist, limit=6):
        """
        Returns the albums of an artist.
        """
        if isinstance(item, Artist):
            return AlbumStore.get_albums_by_artisthash(item.artisthash)[:limit]

        return []

    @staticmethod
    def fill(items: list, extra: list, key: str, limit: int) -> list:
        """
        Appends unseen entries from `extra` to `items` until `limit` is reached.
        """
        seen = {getattr(item, key) for item in items}

        for item in extra:
            if len(items) >= limit:
                break

            if getattr(item, key) not in seen:
                items.append(item)
                seen.add(getattr(item, key))

        return items

    @staticmethod
    def search(query: str, limit: int):
        tracks = SearchTracks(query)(limit=TopResults.TRACKS_LIMIT)
        albums = SearchAlbums(query)(limit=limit)
        artists = SearchArtists(query)(limit=limit)

        # INFO: On equal scores, artists win over tracks, which win over albums
        all_results = sorted(artists + tracks + albums, key=lambda x: x._score, reverse=True)

        if not all_results:
            return {
                "top_result": None,
                "tracks": [],
                "artists": [],
                "albums": [],
            }

        top_result = all_results[0]

        top_tracks = TopResults.get_track_items(top_result, limit=TopResults.TRACKS_LIMIT)
        top_tracks = TopResults.fill(top_tracks, tracks, "trackhash", TopResults.TRACKS_LIMIT)

        top_albums = TopResults.get_album_items(top_result, limit=limit)
        top_albums = TopResults.fill(top_albums, albums, "albumhash", limit)

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
            "tracks": serialize_tracks(top_tracks),
            "artists": serialize_for_cards(artists),
            "albums": serialize_albums(top_albums),
        }
