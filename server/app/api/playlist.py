"""
Contains all the playlist routes.
"""

from flask import Blueprint, request
from app import instances, api
from app.lib import playlistlib

playlist_bp = Blueprint("playlist", __name__, url_prefix="/")


@playlist_bp.route("/playlists", methods=["GET"])
def get_all_playlists():
    playlists = []
    for playlist in api.PLAYLISTS:
        del playlist.tracks
        playlists.append(playlist)

    return playlists


@playlist_bp.route("/playlist/new")
def create_playlist():
    data = request.get_json()

    playlist = {"name": data["name"], "description": data["description"], "tracks": []}

    instances.playlist_instance.insert_playlist(playlist)
    return 200


@playlist_bp.route("/playlist/<playlist_id>/add", methods=["POST"])
def add_track_to_playlist(playlist_id):
    data = request.get_json()

    pid = data["playlist"]
    trackid = data["track"]

    playlistlib.add_track(pid, trackid)
    return 200
