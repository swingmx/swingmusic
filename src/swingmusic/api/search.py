"""
Contains all the search routes.
"""

from typing import Any, Literal
from unidecode import unidecode
from pydantic import Field
from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint

from swingmusic import models
from swingmusic.api.apischemas import GenericLimitSchema
from swingmusic.lib import searchlib
from swingmusic.serializers.artist import serialize_for_cards
from swingmusic.settings import Defaults
from swingmusic.store.tracks import TrackStore


tag = Tag(name="Search", description="Search for tracks, albums and artists")
api = APIBlueprint("search", __name__, url_prefix="/search", abp_tags=[tag])

SEARCH_COUNT = 30
HASH_QUERY_LENGTH = 16
"""
The max amount of items to return per request
"""


class SearchQuery(GenericLimitSchema):
    q: str = Field(
        description="The search query",
        json_schema_extra={"example": "Fleetwood Mac"},
    )
    start: int = Field(description="The index to start from", default=0)
    limit: int = Field(
        description="The number of items to return", default=SEARCH_COUNT
    )


class TopResultsQuery(SearchQuery):
    limit: int = Field(
        description="The number of items to return", default=Defaults.API_CARD_LIMIT
    )


class SearchLoadMoreQuery(SearchQuery):
    itemtype: Literal["tracks", "albums", "artists"] = Field(
        description="The type of search",
        json_schema_extra={"example": "tracks"},
    )


class Search:
    def __init__(self, query: str) -> None:
        self.tracks: list[models.Track] = []
        self.query = unidecode(query)

    def _is_hash_query(self) -> bool:
        return len(self.query) == HASH_QUERY_LENGTH

    def _search_tracks_by_hash(self):
        if not self._is_hash_query():
            return None

        group = TrackStore.trackhashmap.get(self.query)
        if group:
            return group.tracks

        return []

    def _search_artist_by_hash(self):
        if not self._is_hash_query():
            return None

        from swingmusic.store.artists import ArtistStore

        artist = ArtistStore.get_artist_by_hash(self.query)
        if artist:
            return serialize_for_cards([artist])

        return []

    def _search_album_by_hash(self):
        if not self._is_hash_query():
            return None

        from swingmusic.serializers.album import serialize_for_card_many
        from swingmusic.store.albums import AlbumStore

        album = AlbumStore.get_album_by_hash(self.query)
        if album:
            return serialize_for_card_many([album])

        return []

    def search_tracks(self):
        """
        Calls :class:`SearchTracks` which returns the tracks that fuzzily match
        the search terms. Then adds them to the `SearchResults` store.
        """
        tracks = self._search_tracks_by_hash()
        if tracks is not None:
            return tracks

        self.tracks = TrackStore.get_flat_list()
        return searchlib.TopResults().search(self.query, tracks_only=True)

    def search_artists(self):
        """Calls :class:`SearchArtists` which returns the artists that fuzzily match
        the search term. Then adds them to the `SearchResults` store.
        """
        artists = self._search_artist_by_hash()
        if artists is not None:
            return artists

        return serialize_for_cards(searchlib.SearchArtists(self.query)())

    def search_albums(self):
        """Calls :class:`SearchAlbums` which returns the albums that fuzzily match
        the search term. Then adds them to the `SearchResults` store.
        """
        albums = self._search_album_by_hash()
        if albums is not None:
            return albums

        return searchlib.TopResults().search(self.query, albums_only=True)

    def get_top_results(
        self,
        limit: int,
    ):
        finder = searchlib.TopResults()
        return finder.search(self.query, limit=limit)


@api.get("/top")
def get_top_results(query: TopResultsQuery):
    """
    Get top results

    Returns the top results for the given query.
    """
    if not query.q:
        return {"error": "No query provided"}, 400

    return Search(query.q).get_top_results(limit=query.limit)


@api.get("/")
def search_items(query: SearchLoadMoreQuery):
    """
    Find tracks, albums or artists from a search query.
    """
    results: Any = []

    match query.itemtype:
        case "tracks":
            results = Search(query.q).search_tracks()
        case "albums":
            results = Search(query.q).search_albums()
        case "artists":
            results = Search(query.q).search_artists()
        case _:
            return {
                "error": "Invalid item type. Valid types are 'tracks', 'albums' and 'artists'"
            }, 400

    return {
        "results": results[query.start : query.start + query.limit],
        "more": len(results) > query.start + query.limit,
    }


# TODO: Rewrite this file using generators where possible
