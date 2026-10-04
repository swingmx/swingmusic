"""
Contains all the search routes.
"""

from typing import Any, Literal
from pydantic import Field
from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint

from swingmusic import models
from swingmusic.api.apischemas import GenericLimitSchema
from swingmusic.lib import searchlib
from swingmusic.serializers.album import serialize_for_card_many as serialize_albums
from swingmusic.serializers.artist import serialize_for_cards
from swingmusic.serializers.track import serialize_tracks
from swingmusic.settings import Defaults


tag = Tag(name="Search", description="Search for tracks, albums and artists")
api = APIBlueprint("search", __name__, url_prefix="/search", abp_tags=[tag])

SEARCH_COUNT = 30
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
        self.query = query

    def search_tracks(self):
        """
        Returns the tracks that fuzzily match the query.
        """
        return serialize_tracks(searchlib.SearchTracks(self.query)())

    def search_artists(self):
        """
        Returns the artists that fuzzily match the query.
        """
        return serialize_for_cards(searchlib.SearchArtists(self.query)())

    def search_albums(self):
        """
        Returns the albums that fuzzily match the query.
        """
        return serialize_albums(searchlib.SearchAlbums(self.query)())

    def get_top_results(self, limit: int):
        return searchlib.TopResults.search(self.query, limit=limit)


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
