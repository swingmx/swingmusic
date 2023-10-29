from flask import Blueprint, request

from app.lib.lyrics import get_lyrics

api = Blueprint("lyrics", __name__, url_prefix="")


@api.route("/lyrics", methods=["POST"])
def send_lyrics():
    """
    Returns the lyrics for a track
    """
    data = request.get_json()

    filepath = data.get("filepath", None)

    if filepath is None:
        return {"error": "No filepath provided"}, 400

    lyrics = get_lyrics(filepath)

    if lyrics is None:
        return {"error": "No lyrics found"}, 204

    return {"lyrics": lyrics}, 200
