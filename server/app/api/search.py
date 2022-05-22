"""
Contains all the search routes.
"""

from flask import Blueprint, request

from app.lib import searchlib
from app import helpers

search_bp = Blueprint("search", __name__, url_prefix="/")

SEARCH_RESULTS = {
    "tracks": [],
    "albums": [],
    "artists": [],
}


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
    start = int(request.args.get("start"))

    print(type, start)

    if type == "tracks":
        return {
            "tracks": SEARCH_RESULTS["tracks"][start : start + 5],
            "more": len(SEARCH_RESULTS["tracks"]) > start + 5,
        }

    elif type == "albums":
        return {
            "albums": SEARCH_RESULTS["albums"][start : start + 6],
            "more": len(SEARCH_RESULTS["albums"]) > start + 6,
        }

    elif type == "artists":
        return {
            "artists": SEARCH_RESULTS["artists"][start : start + 6],
            "more": len(SEARCH_RESULTS["artists"]) > start + 6,
        }
