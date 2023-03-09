"""
Contains all the search routes.
"""

from unidecode import unidecode
from flask import Blueprint, request

from app import models
from app.db.store import Store
from app.lib import searchlib

api = Blueprint("search", __name__, url_prefix="/")

SEARCH_COUNT = 12
"""The max amount of items to return per request"""


class SearchResults:
    """
    Holds all the search results.
    """

    query: str = ""
    tracks: list[models.Track] = []
    albums: list[models.Album] = []
    playlists: list[models.Playlist] = []
    artists: list[models.Artist] = []


class Search:
    def __init__(self, query: str) -> None:
        self.tracks: list[models.Track] = []
        self.query = unidecode(query)
        SearchResults.query = self.query

    def search_tracks(self):
        """
        Calls :class:`SearchTracks` which returns the tracks that fuzzily match
        the search terms. Then adds them to the `SearchResults` store.
        """
        self.tracks = Store.tracks
        tracks = searchlib.SearchTracks(self.query)()

        SearchResults.tracks = tracks
        return tracks

    def search_artists(self):
        """Calls :class:`SearchArtists` which returns the artists that fuzzily match
        the search term. Then adds them to the `SearchResults` store.
        """
        artists = searchlib.SearchArtists(self.query)()
        SearchResults.artists = artists
        return artists

    def search_albums(self):
        """Calls :class:`SearchAlbums` which returns the albums that fuzzily match
        the search term. Then adds them to the `SearchResults` store.
        """
        albums = searchlib.SearchAlbums(self.query)()
        SearchResults.albums = albums

        return albums

    # def search_playlists(self):
    #     """Calls :class:`SearchPlaylists` which returns the playlists that fuzzily match
    #     the search term. Then adds them to the `SearchResults` store.
    #     """
    #     playlists = utils.Get.get_all_playlists()
    #     playlists = [serializer.Playlist(playlist) for playlist in playlists]

    #     playlists = searchlib.SearchPlaylists(playlists, self.query)()
    #     SearchResults.playlists = playlists

    #     return playlists

    def get_top_results(self):
        finder = searchlib.SearchAll()
        return finder.search(self.query)

    def search_all(self):
        """Calls all the search methods."""
        self.search_tracks()
        self.search_albums()
        self.search_artists()
        # self.search_playlists()


@api.route("/search/tracks", methods=["GET"])
def search_tracks():
    """
    Searches for tracks that match the search query.
    """

    query = request.args.get("q")
    if not query:
        return {"error": "No query provided"}, 400

    tracks = Search(query).search_tracks()

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
    if not query:
        return {"error": "No query provided"}, 400

    tracks = Search(query).search_albums()

    return {
        "albums": tracks[:SEARCH_COUNT],
        "more": len(tracks) > SEARCH_COUNT,
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


# @searchbp.route("/search/playlists", methods=["GET"])
# def search_playlists():
#     """
#     Searches for playlists.
#     """

#     query = request.args.get("q")
#     if not query:
#         return {"error": "No query provided"}, 400

#     playlists = DoSearch(query).search_playlists()

#     return {
#         "playlists": playlists[:SEARCH_COUNT],
#         "more": len(playlists) > SEARCH_COUNT,
#     }


@api.route("/search/top", methods=["GET"])
def get_top_results():
    """
    Returns the top results for the search query.
    """

    query = request.args.get("q")
    if not query:
        return {"error": "No query provided"}, 400

    results = Search(query).get_top_results()

    # max_results = 2
    # return {
    #     "tracks": SearchResults.tracks[:max_results],
    #     "albums": SearchResults.albums[:max_results],
    #     "artists": SearchResults.artists[:max_results],
    #     "playlists": SearchResults.playlists[:max_results],
    # }
    return {
        "results": results
    }


@api.route("/search/loadmore")
def search_load_more():
    """
    Returns more songs, albums or artists from a search query.
    """
    s_type = request.args.get("type")
    index = int(request.args.get("index") or 0)

    if s_type == "tracks":
        t = SearchResults.tracks
        return {
            "tracks": t[index: index + SEARCH_COUNT],
            "more": len(t) > index + SEARCH_COUNT,
        }

    elif s_type == "albums":
        a = SearchResults.albums
        return {
            "albums": a[index: index + SEARCH_COUNT],
            "more": len(a) > index + SEARCH_COUNT,
        }

    elif s_type == "artists":
        a = SearchResults.artists
        return {
            "artists": a[index: index + SEARCH_COUNT],
            "more": len(a) > index + SEARCH_COUNT,
        }
