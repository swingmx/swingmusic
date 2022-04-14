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
        filepath = [
            file["filepath"]
            for file in api.PRE_TRACKS
            if file["_id"]["$oid"] == trackid
        ][0]
    except (FileNotFoundError, IndexError) as e:
        return "File not found", 404

    return send_file(filepath, mimetype="audio/mp3")


@track_bp.route("/sample")
def get_sample_track():
    """
    Returns a sample track object.
    """

    return instances.songs_instance.get_song_by_album("Legends Never Die", "Juice WRLD")
