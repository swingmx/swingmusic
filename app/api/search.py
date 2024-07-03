"""
Contains all the search routes.
"""

from unidecode import unidecode
from pydantic import Field
from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint

from app import models
from app.api.apischemas import GenericLimitSchema
from app.db.libdata import TrackTable
from app.lib import searchlib
from app.settings import Defaults


tag = Tag(name="Search", description="Search for tracks, albums and artists")
api = APIBlueprint("search", __name__, url_prefix="/search", abp_tags=[tag])

SEARCH_COUNT = 30
"""The max amount of items to return per request"""


class Search:
    def __init__(self, query: str) -> None:
        self.tracks: list[models.Track] = []
        self.query = unidecode(query)

    def search_tracks(self):
        """
        Calls :class:`SearchTracks` which returns the tracks that fuzzily match
        the search terms. Then adds them to the `SearchResults` store.
        """
        self.tracks = TrackTable.get_all()
        return searchlib.TopResults().search(self.query, tracks_only=True)

    def search_artists(self):
        """Calls :class:`SearchArtists` which returns the artists that fuzzily match
        the search term. Then adds them to the `SearchResults` store.
        """
        return searchlib.SearchArtists(self.query)()

    def search_albums(self):
        """Calls :class:`SearchAlbums` which returns the albums that fuzzily match
        the search term. Then adds them to the `SearchResults` store.
        """
        return searchlib.TopResults().search(self.query, albums_only=True)

    def get_top_results(
        self,
        limit: int,
    ):
        finder = searchlib.TopResults()
        return finder.search(self.query, limit=limit)


class SearchQuery(GenericLimitSchema):
    q: str = Field(description="The search query", example=Defaults.API_ARTISTNAME)
    start: int = Field(description="The index to start from", default=0, example=0)


@api.get("/tracks")
def search_tracks(query: SearchQuery):
    """
    Search tracks
    """
    tracks = Search(query.q).search_tracks()

    return {
        "tracks": tracks[:SEARCH_COUNT],
        "more": len(tracks) > SEARCH_COUNT,
    }


@api.get("/albums")
def search_albums(
    query: SearchQuery,
):
    """
    Search albums.
    """
    albums = Search(query.q).search_albums()

    return {
        "albums": albums[:SEARCH_COUNT],
        "more": len(albums) > SEARCH_COUNT,
    }


@api.get("/artists")
def search_artists(query: SearchQuery):
    """
    Search artists.
    """
    if not query.q:
        return {"error": "No query provided"}, 400

    artists = Search(query.q).search_artists()

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
    if not query.q:
        return {"error": "No query provided"}, 400

    return Search(query.q).get_top_results(limit=query.limit)


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

    if item_type == "tracks":
        t = Search(query).search_tracks()
        return {
            "tracks": t[index : index + SEARCH_COUNT],
            "more": len(t) > index + SEARCH_COUNT,
        }

    elif item_type == "albums":
        a = Search(query).search_albums()
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
