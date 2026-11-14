"""
This library contains all the functions related to the search functionality.
"""

from typing import Any

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


def fuzzy_match(query: str, choices: list[str], cutoff: int, limit: int | None = None) -> list[tuple[float, int]]:
    """
    Returns (score, index) pairs for choices matching the query, best first.
    """
    results: list[tuple[float, int]] = []

    for choice, score, index in process.extract(query, choices, scorer=fuzz.WRatio, score_cutoff=cutoff, limit=None):
        # WRatio scores a short choice found inside the query (eg. "iri" in "nviiri") as a near match
        if len(query) >= 1.5 * len(choice):
            score = fuzz.ratio(query, choice)

        if score >= cutoff:
            results.append((score, index))

    results.sort(key=lambda r: r[0], reverse=True)
    return results[:limit]


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

    scores: dict[int, float] = {}

    for score, position in fuzzy_match(query, haystack, cutoff):
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

        artists: list[Artist] = []

        for score, index in fuzzy_match(self.query, choices, Cutoff.artists, limit):
            artist = self.artists[index]
            artist._score = score
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
        playlists: list[Playlist] = []

        for score, index in fuzzy_match(self.query, choices, Cutoff.playlists, limit):
            playlist = self.playlists[index]
            playlist._score = score
            playlists.append(playlist)

        return playlists


def classical_search():
    """
    The classical search module when classical support is on, else None.
    """
    try:
        from swingmusic.config import UserConfig
        from swingmusic.premium import classical_available

        if not classical_available():
            return None
        from swingmusic.premium.classical import search

        return search
    except Exception:  # noqa: BLE001
        return None


def merge_people(artists: list[Artist], people: list[tuple[float, dict]], limit: int) -> list[dict]:
    """
    Library artists and classical people as artist cards, best first, each
    hash once; a person wins a tie with an artist.
    """
    scored = [(score, 0, card) for score, card in people]
    scored += [(a._score, 1, serialize_for_card(a)) for a in artists]
    scored.sort(key=lambda row: (-row[0], row[1]))
    cards: list[dict] = []
    seen: set[str] = set()
    for _, _, card in scored:
        if card["artisthash"] not in seen:
            seen.add(card["artisthash"])
            cards.append(card)
    return cards[:limit]


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
    def search(query: str, limit: int, classical: bool = False):
        cs = classical_search() if classical else None
        if cs is not None:
            return TopResults.search_classical(cs, query, limit)

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

    @staticmethod
    def classical_top(cs, query: str, limit: int):
        """
        The top result with composers, performers, works and movements
        competing for it, with the item it came from, the searched tracks,
        albums and artists, and the classical hits.
        """
        tracks = SearchTracks(query)()
        albums = SearchAlbums(query)(limit=limit)
        artists = SearchArtists(query)(limit=limit)
        hits = cs.classical_hits(query)

        # equal scores: people, then artists, then works and movements, then tracks, then albums
        candidates: list[tuple[float, int, str, Any]] = [
            (hit.score, 0, "person", hit) for hit in hits if hit.kind in ("composer", "performer")
        ]
        candidates += [(a._score, 1, "artist", a) for a in artists]
        candidates += [(hit.score, 2, "classical", hit) for hit in hits if hit.kind in ("work", "movement")]
        candidates += [(t._score, 3, "track", t) for t in tracks[: TopResults.TRACKS_LIMIT]]
        candidates += [(a._score, 4, "album", a) for a in albums]
        candidates.sort(key=lambda row: (-row[0], row[1]))

        top_result, top_item = None, None
        for score, _, kind, item in candidates:
            if kind in ("person", "classical"):
                top_result = cs.top_payload(item)
            elif kind == "track" and item.trackhash in cs.ClassicalStore.trackmap:
                top_result = cs.top_payload(cs.Hit("movement", item.trackhash, score))
            elif kind == "track":
                top_result = {**serialize_track(item), "type": "track"}
            elif kind == "artist":
                top_result = {**serialize_for_card(item, include={"albumcount", "trackcount"}), "type": "artist"}
            else:
                top_result = {**serialize_album(item), "type": "album"}
            if top_result is not None:
                top_item = item
                break

        return top_result, top_item, tracks, albums, artists, hits

    @staticmethod
    def search_classical(cs, query: str, limit: int):
        """
        Top results with composers, performers, works and movements
        competing for the top spot, and the top works.
        """
        top_result, item, tracks, albums, artists, hits = TopResults.classical_top(cs, query, limit)
        if top_result is None:
            return {"top_result": None, "tracks": [], "works": [], "artists": [], "albums": []}

        top_tracks = cs.track_results(tracks, hits, top_result, query)
        if top_result["type"] in ("artist", "album"):
            own = TopResults.get_track_items(item, limit=TopResults.TRACKS_LIMIT)
            top_tracks = TopResults.fill(own, top_tracks, "trackhash", TopResults.TRACKS_LIMIT)
        top_albums = TopResults.get_album_items(item, limit=limit) if top_result["type"] == "artist" else []
        top_albums = TopResults.fill(top_albums, albums, "albumhash", limit)

        # a composer on top shows their works in place of tracks
        works = []
        if top_result["type"] == "composer":
            works = cs.serialize_works(cs.work_results(hits, top_result)[: TopResults.TRACKS_LIMIT])
        return {
            "top_result": top_result,
            "tracks": [] if works else cs.serialize_tracks(top_tracks[: TopResults.TRACKS_LIMIT]),
            "works": works,
            "artists": merge_people(artists, cs.people(hits), limit),
            "albums": serialize_albums(top_albums),
        }
