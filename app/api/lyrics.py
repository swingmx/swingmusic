from flask import Blueprint, request

from app.lib.lyrics import get_lyrics, check_lyrics_file, get_lyrics_from_duplicates

api = Blueprint("lyrics", __name__, url_prefix="")


@api.route("/lyrics", methods=["POST"])
def send_lyrics():
    """
    Returns the lyrics for a track
    """
    data = request.get_json()

    filepath = data.get("filepath", None)
    trackhash = data.get("trackhash", None)

    if filepath is None or trackhash is None:
        return {"error": "No filepath or trackhash provided"}, 400

    lyrics = get_lyrics(filepath)

    if lyrics is None:
        lyrics = get_lyrics_from_duplicates(trackhash, filepath)

    if lyrics is None:
        return {"error": "No lyrics found"}, 204

    return {"lyrics": lyrics}, 200


@api.route("/lyrics/check", methods=["POST"])
def check_lyrics():
    data = request.get_json()

    filepath = data.get("filepath", None)
    trackhash = data.get("trackhash", None)

    if filepath is None or trackhash is None:
        return {"error": "No filepath or trackhash provided"}, 400

    exists, filepath = check_lyrics_file(filepath, trackhash)

    if exists:
        return {"filepath": filepath}, 200
