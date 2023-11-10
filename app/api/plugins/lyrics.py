from flask import Blueprint, request
from app.lib.lyrics import format_synced_lyrics

from app.plugins.lyrics import Lyrics
from app.utils.hashing import create_hash

api = Blueprint("lyricsplugin", __name__, url_prefix="/plugins/lyrics")


@api.route("/search", methods=["POST"])
def search_lyrics():
    data = request.get_json()

    trackhash = data.get("trackhash", "")
    title = data.get("title", "")
    artist = data.get("artist", "")
    album = data.get("album", "")
    filepath = data.get("filepath", None)

    finder = Lyrics()

    data = finder.search_lyrics_by_title_and_artist(title, artist)

    if not data:
        return {"trackhash": trackhash, "lyrics": None}

    perfect_match = data[0]

    for track in data:
        i_title = track["title"]
        i_album = track["album"]

        if create_hash(i_title) == create_hash(title) and create_hash(
            i_album
        ) == create_hash(album):
            perfect_match = track

    track_id = perfect_match["track_id"]
    lrc = finder.download_lyrics(track_id, filepath)

    if lrc is not None:
        lines = lrc.split("\n")
        lyrics = format_synced_lyrics(lines)

        return {"trackhash": trackhash, "lyrics": lyrics}, 200

    return {"trackhash": trackhash, "lyrics": lrc}, 200
