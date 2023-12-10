"""
Contains all the search routes.
"""

from flask import Blueprint, request
from unidecode import unidecode

from app import models
from app.lib import searchlib
from app.store.tracks import TrackStore

api = Blueprint("search", __name__, url_prefix="/")

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


@api.route("/search/tracks", methods=["GET"])
def search_tracks():
    """
    Searches for tracks that match the search query.
    """

    query = request.args.get("q")
    in_quotes = query_in_quotes(query)

    if not query:
        return {"error": "No query provided"}, 400

    tracks = Search(query).search_tracks(in_quotes)

    return {
        "tracks": tracks[:SEARCH_COUNT],
        "more": len(tracks) > SEARCH_COUNT,
    }


@api.route("/search/albums", methods=["GET"])
def search_albums():
    """
    Searches for albums.
    """

    query = request.args.get("q")
    in_quotes = query_in_quotes(query)

    if not query:
        return {"error": "No query provided"}, 400

    albums = Search(query).search_albums(in_quotes)

    return {
        "albums": albums[:SEARCH_COUNT],
        "more": len(albums) > SEARCH_COUNT,
    }


@api.route("/search/artists", methods=["GET"])
def search_artists():
    """
    Searches for artists.
    """

    query = request.args.get("q")

    if not query:
        return {"error": "No query provided"}, 400

    artists = Search(query).search_artists()

    return {
        "artists": artists[:SEARCH_COUNT],
        "more": len(artists) > SEARCH_COUNT,
    }


@api.route("/search/top", methods=["GET"])
def get_top_results():
    """
    Returns the top results for the search query.
    """

    query = request.args.get("q")
    limit = request.args.get("limit", "6")
    limit = int(limit)

    in_quotes = query_in_quotes(query)

    if not query:
        return {"error": "No query provided"}, 400

    return Search(query).get_top_results(in_quotes=in_quotes, limit=limit)


@api.route("/search/loadmore")
def search_load_more():
    """
    Returns more songs, albums or artists from a search query.
    """
    query = request.args.get("q")
    in_quotes = query_in_quotes(query)

    s_type = request.args.get("type")
    index = int(request.args.get("index") or 0)

    if s_type == "tracks":
        t = Search(query).search_tracks(in_quotes)
        return {
            "tracks": t[index : index + SEARCH_COUNT],
            "more": len(t) > index + SEARCH_COUNT,
        }

    elif s_type == "albums":
        a = Search(query).search_albums(in_quotes)
        return {
            "albums": a[index : index + SEARCH_COUNT],
            "more": len(a) > index + SEARCH_COUNT,
        }

    elif s_type == "artists":
        a = Search(query).search_artists()
        return {
            "artists": a[index : index + SEARCH_COUNT],
            "more": len(a) > index + SEARCH_COUNT,
        }


# TODO: Rewrite this file using generators where possible
