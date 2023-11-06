from flask import Blueprint, request

from app.lib.lyrics import (
    get_lyrics,
    check_lyrics_file,
    get_lyrics_from_duplicates,
    get_lyrics_from_tags,
)

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

    is_synced = True
    lyrics, copyright = get_lyrics(filepath)

    if not lyrics:
        lyrics, copyright = get_lyrics_from_duplicates(trackhash, filepath)

    if not lyrics:
        lyrics, is_synced, copyright = get_lyrics_from_tags(filepath)

    if not lyrics:
        return {"error": "No lyrics found"}

    return {"lyrics": lyrics, "synced": is_synced, "copyright": copyright}, 200


@api.route("/lyrics/check", methods=["POST"])
def check_lyrics():
    data = request.get_json()

    filepath = data.get("filepath", None)
    trackhash = data.get("trackhash", None)

    if filepath is None or trackhash is None:
        return {"error": "No filepath or trackhash provided"}, 400

    exists = check_lyrics_file(filepath, trackhash)

    if exists:
        return {"exists": exists}, 200

    exists = get_lyrics_from_tags(filepath, just_check=True)

    return {"exists": exists}, 200

