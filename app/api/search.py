"""
Contains all the search routes.
"""

from flask import request
from unidecode import unidecode
from pydantic import BaseModel, Field
from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint

from app import models
from app.lib import searchlib
from app.settings import Defaults
from app.store.tracks import TrackStore

tag = Tag(name="Search", description="Search for tracks, albums and artists")
api = APIBlueprint("search", __name__, url_prefix="/search", abp_tags=[tag])

SEARCH_COUNT = 30
"""The max amount of items to return per request"""


def query_in_quotes(query: str) -> bool:
    """
    Returns True if the query is in quotes
    """
    try:
        return query.startswith('"') and query.endswith('"')
    except AttributeError:
        return False


class Search:
    def __init__(self, query: str) -> None:
        self.tracks: list[models.Track] = []
        self.query = unidecode(query)

    def search_tracks(self, in_quotes=False):
        """
        Calls :class:`SearchTracks` which returns the tracks that fuzzily match
        the search terms. Then adds them to the `SearchResults` store.
        """
        self.tracks = TrackStore.tracks
        return searchlib.TopResults().search(
            self.query, tracks_only=True, in_quotes=in_quotes
        )

    def search_artists(self):
        """Calls :class:`SearchArtists` which returns the artists that fuzzily match
        the search term. Then adds them to the `SearchResults` store.
        """
        return searchlib.SearchArtists(self.query)()

    def search_albums(self, in_quotes=False):
        """Calls :class:`SearchAlbums` which returns the albums that fuzzily match
        the search term. Then adds them to the `SearchResults` store.
        """
        return searchlib.TopResults().search(
            self.query, albums_only=True, in_quotes=in_quotes
        )

    def get_top_results(
        self,
        limit: int,
        in_quotes=False,
    ):
        finder = searchlib.TopResults()
        return finder.search(self.query, in_quotes=in_quotes, limit=limit)


class SearchQuery(BaseModel):
    q: str = Field(description="The search query", example=Defaults.API_ARTISTNAME)


@api.get("/tracks")
def search_tracks(query: SearchQuery):
    """
    Search tracks
    """

    query = query.q
    in_quotes = query_in_quotes(query)

    tracks = Search(query).search_tracks(in_quotes)

    return {
        "tracks": tracks[:SEARCH_COUNT],
        "more": len(tracks) > SEARCH_COUNT,
    }


@api.get("/albums")
def search_albums(query: SearchQuery):
    """
    Search albums.
    """

    query = query.q
    in_quotes = query_in_quotes(query)

    albums = Search(query).search_albums(in_quotes)

    return {
        "albums": albums[:SEARCH_COUNT],
        "more": len(albums) > SEARCH_COUNT,
    }


@api.get("/artists")
def search_artists(query: SearchQuery):
    """
    Search artists.
    """

    query = query.q

    if not query:
        return {"error": "No query provided"}, 400

    artists = Search(query).search_artists()

    return {
        "artists": artists[:SEARCH_COUNT],
        "more": len(artists) > SEARCH_COUNT,
    }


class TopResultsQuery(SearchQuery):
    limit: int = Field(
        description="The number of items to return", default=Defaults.API_CARD_LIMIT
    )


@api.get("/top")
def get_top_results(query: TopResultsQuery):
    """
    Get top results

    Returns the top results for the given query.
    """

    query = query.q
    limit = query.limit

    in_quotes = query_in_quotes(query)

    if not query:
        return {"error": "No query provided"}, 400

    return Search(query).get_top_results(in_quotes=in_quotes, limit=limit)


class SearchLoadMoreQuery(SearchQuery):
    type: str = Field(description="The type of search", example="tracks")
    index: int = Field(description="The index to start from", default=0)


@api.get("/loadmore")
def search_load_more(query: SearchLoadMoreQuery):
    """
    Load more

    Returns more songs, albums or artists from a search query.

    NOTE: You must first initiate a search using the `/search` endpoint.
    """
    query = query.q
    item_type = query.type
    index = query.index
    in_quotes = query_in_quotes(query)

    if item_type == "tracks":
        t = Search(query).search_tracks(in_quotes)
        return {
            "tracks": t[index : index + SEARCH_COUNT],
            "more": len(t) > index + SEARCH_COUNT,
        }

    elif item_type == "albums":
        a = Search(query).search_albums(in_quotes)
        return {
            "albums": a[index : index + SEARCH_COUNT],
            "more": len(a) > index + SEARCH_COUNT,
        }

    elif item_type == "artists":
        a = Search(query).search_artists()
        return {
            "artists": a[index : index + SEARCH_COUNT],
            "more": len(a) > index + SEARCH_COUNT,
        }


# TODO: Rewrite this file using generators where possible
