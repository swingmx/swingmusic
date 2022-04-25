"""
Contains all the track routes.
"""
from app import api
from app import instances
from flask import Blueprint
from flask import send_file

track_bp = Blueprint("track", __name__, url_prefix="/")


@track_bp.route("/file/<trackid>")
def send_track_file(trackid):
    """
    Returns an audio file that matches the passed id to the client.
    """
    try:
        files = []
        for f in api.DB_TRACKS:
            try:
                if f["_id"]["$oid"] == trackid:
                    files.append(f["filepath"])
            except KeyError:
                # Bug: some albums are not found although they exist in `api.ALBUMS`. It has something to do with the bisection method used or sorting. Not sure yet.
                pass

        filepath = files[0]
    except IndexError:
        return "File not found", 404

    return send_file(filepath, mimetype="audio/mp3")


@track_bp.route("/sample")
def get_sample_track():
    """
    Returns a sample track object.
    """

    return instances.tracks_instance.get_song_by_album(
        "Legends Never Die", "Juice WRLD"
    )
