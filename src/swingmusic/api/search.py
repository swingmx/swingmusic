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
    classical: bool = Field(
        description="Include composers, performers, works and movements, and label classical tracks with their works",
        default=False,
    )


class TopResultsQuery(SearchQuery):
    limit: int = Field(
        description="The number of items to return", default=Defaults.API_CARD_LIMIT
    )


class SearchLoadMoreQuery(SearchQuery):
    itemtype: Literal["tracks", "movements", "works", "albums", "artists"] = Field(
        description="The type of search",
        json_schema_extra={"example": "tracks"},
    )


class Search:
    def __init__(self, query: str, classical: bool = False) -> None:
        self.query = query
        self.classical = searchlib.classical_search() if classical else None

    def search_tracks(self, start: int, limit: int, movements: bool = False):
        """
        The page of tracks that fuzzily match the query and whether more
        follow. With classical on, `movements` picks the classical tracks
        alone, ordered by the top result, else the non-classical ones.
        """
        cs = self.classical
        if cs is None:
            if movements:
                return [], False
            tracks = searchlib.SearchTracks(self.query)()
            return serialize_tracks(tracks[start : start + limit]), len(tracks) > start + limit
        top, _, tracks, _, _, hits = searchlib.TopResults.classical_top(cs, self.query, SEARCH_COUNT)
        tracks = [
            t
            for t in cs.track_results(tracks, hits, top, self.query)
            if (t.trackhash in cs.ClassicalStore.trackmap) == movements
        ]
        return cs.serialize_tracks(tracks[start : start + limit]), len(tracks) > start + limit

    def search_works(self, start: int, limit: int):
        """
        The page of works that match the query, a composer top result's own
        works first, and whether more follow.
        """
        cs = self.classical
        if cs is None:
            return [], False
        top, _, _, _, _, hits = searchlib.TopResults.classical_top(cs, self.query, SEARCH_COUNT)
        works = cs.work_results(hits, top)
        return cs.serialize_works(works[start : start + limit]), len(works) > start + limit

    def search_artists(self):
        """
        Returns the artists that fuzzily match the query, with composers and
        performers when asked.
        """
        artists = searchlib.SearchArtists(self.query)()
        cs = self.classical
        if cs is None:
            return serialize_for_cards(artists)
        return searchlib.merge_people(artists, cs.people(cs.classical_hits(self.query)), searchlib.Limit.artists)

    def search_albums(self):
        """
        Returns the albums that fuzzily match the query.
        """
        return serialize_albums(searchlib.SearchAlbums(self.query)())

    def get_top_results(self, limit: int):
        return searchlib.TopResults.search(self.query, limit=limit, classical=self.classical is not None)


@api.get("/top")
def get_top_results(query: TopResultsQuery):
    """
    Get top results

    Returns the top results for the given query.
    """
    if not query.q:
        return {"error": "No query provided"}, 400

    return Search(query.q, query.classical).get_top_results(limit=query.limit)


@api.get("/")
def search_items(query: SearchLoadMoreQuery):
    """
    Find tracks, movements, works, albums or artists from a search query.
    """
    results: Any = []

    search = Search(query.q, query.classical)
    match query.itemtype:
        case "tracks" | "movements":
            page, more = search.search_tracks(query.start, query.limit, query.itemtype == "movements")
            return {"results": page, "more": more}
        case "works":
            page, more = search.search_works(query.start, query.limit)
            return {"results": page, "more": more}
        case "albums":
            results = search.search_albums()
        case "artists":
            results = search.search_artists()
        case _:
            return {
                "error": "Invalid item type. Valid types are 'tracks', 'movements', 'works', 'albums' and 'artists'"
            }, 400

    return {
        "results": results[query.start : query.start + query.limit],
        "more": len(results) > query.start + query.limit,
    }


# TODO: Rewrite this file using generators where possible
