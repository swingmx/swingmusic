"""
Contains all the track routes.
"""
import os

from flask import Blueprint, send_file, request

from app.store.tracks import TrackStore

api = Blueprint("track", __name__, url_prefix="/")


@api.route("/file/<trackhash>")
def send_track_file(trackhash: str):
    """
    Returns an audio file that matches the passed id to the client.
    Falls back to track hash if id is not found.
    """
    msg = {"msg": "File Not Found"}

    def get_mime(filename: str) -> str:
        ext = filename.rsplit(".", maxsplit=1)[-1]
        return f"audio/{ext}"

    filepath = request.args.get("filepath")

    if filepath is not None:
        try:
            track = TrackStore.get_tracks_by_filepaths([filepath])[0]
        except IndexError:
            track = None

        track_exists = track is not None and os.path.exists(track.filepath)

        if track_exists:
            audio_type = get_mime(filepath)
            return send_file(filepath, mimetype=audio_type)

    if trackhash is None:
        return msg, 404

    tracks = TrackStore.get_tracks_by_trackhashes([trackhash])

    for track in tracks:
        if track is None:
            return msg, 404

        audio_type = get_mime(track.filepath)

        try:
            return send_file(track.filepath, mimetype=audio_type)
        except FileNotFoundError:
            return msg, 404

    return msg, 404
