"""
Contains all the search routes.
"""

from app import helpers
from app.lib import searchlib
from flask import Blueprint, request

search_bp = Blueprint("search", __name__, url_prefix="/")

SEARCH_RESULTS = {
    "tracks": [],
    "albums": [],
    "artists": [],
}


@search_bp.route("/search/tracks", methods=["GET"])
def search_tracks():
    """
    Searches for tracks.
    """

    query = request.args.get("q")
    if not query:
        return {"error": "No query provided"}, 400

    results = searchlib.SearchTracks(query)()
    SEARCH_RESULTS["tracks"] = results

    return {
        "tracks": results[:5],
        "more": len(results) > 5,
    }, 200


@search_bp.route("/search/albums", methods=["GET"])
def search_albums():
    """
    Searches for albums.
    """

    query = request.args.get("q")
    if not query:
        return {"error": "No query provided"}, 400

    results = searchlib.SearchAlbums(query)()
    SEARCH_RESULTS["albums"] = results

    return {
        "albums": results[:6],
        "more": len(results) > 6,
    }, 200


@search_bp.route("/search/artists", methods=["GET"])
def search_artists():
    """
    Searches for artists.
    """

    query = request.args.get("q")
    if not query:
        return {"error": "No query provided"}, 400

    results = searchlib.SearchArtists(query)()
    SEARCH_RESULTS["artists"] = results

    return {
        "artists": results[:6],
        "more": len(results) > 6,
    }, 200


@search_bp.route("/search")
def search():
    """
    Returns a list of songs, albums and artists that match the search query.
    """
    query = request.args.get("q") or "Mexican girl"

    albums = searchlib.SearchAlbums(query)()
    artists_dicts = searchlib.SearchArtists(query)()

    tracks = searchlib.SearchTracks(query)()
    top_artist = artists_dicts[0]["name"]

    _tracks = searchlib.GetTopArtistTracks(top_artist)()
    tracks = [*tracks, *[t for t in _tracks if t not in tracks]]

    SEARCH_RESULTS.clear()
    SEARCH_RESULTS["tracks"] = tracks
    SEARCH_RESULTS["albums"] = albums
    SEARCH_RESULTS["artists"] = artists_dicts

    return {
        "data": [
            {"tracks": tracks[:5], "more": len(tracks) > 5},
            {"albums": albums[:6], "more": len(albums) > 6},
            {"artists": artists_dicts[:6], "more": len(artists_dicts) > 6},
        ]
    }


@search_bp.route("/search/loadmore")
def search_load_more():
    """
    Returns more songs, albums or artists from a search query.
    """
    type = request.args.get("type")
    index = int(request.args.get("index"))

    print(type, index)
    print(len(SEARCH_RESULTS["tracks"]))

    if type == "tracks":
        return {
            "tracks": SEARCH_RESULTS["tracks"][index : index + 5],
            "more": len(SEARCH_RESULTS["tracks"]) > index + 5,
        }

    elif type == "albums":
        return {
            "albums": SEARCH_RESULTS["albums"][index : index + 6],
            "more": len(SEARCH_RESULTS["albums"]) > index + 6,
        }

    elif type == "artists":
        return {
            "artists": SEARCH_RESULTS["artists"][index : index + 6],
            "more": len(SEARCH_RESULTS["artists"]) > index + 6,
        }
