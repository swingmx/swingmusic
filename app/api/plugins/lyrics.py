from flask import Blueprint, request

from app.plugins.lyrics import Lyrics
from app.utils.hashing import create_hash

api = Blueprint("lyricsplugin", __name__, url_prefix="/plugins/lyrics")


@api.route("/search", methods=["POST"])
def search_lyrics():
    data = request.get_json()

    title = data.get("title", "")
    artist = data.get("artist", "")
    album = data.get("album", "")
    filepath = data.get("filepath", None)

    finder = Lyrics()

    data = finder.search_lyrics_by_title_and_artist(title, artist)

    if not data:
        return {"downloaded": False}

    perfect_match = data[0]

    for track in data:
        i_title = track["title"]
        i_album = track["album"]

        if create_hash(i_title) == create_hash(title) and create_hash(
            i_album
        ) == create_hash(album):
            perfect_match = track

    track_id = perfect_match["track_id"]
    downloaded = finder.download_lyrics(track_id, filepath)

    return {"downloaded": downloaded}, 200
