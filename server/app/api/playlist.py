"""
Contains all the playlist routes.
"""

from flask import Blueprint, request
from app import instances, api
from app.lib import playlistlib
from app import models

playlist_bp = Blueprint("playlist", __name__, url_prefix="/")


@playlist_bp.route("/playlists", methods=["GET"])
def get_all_playlists():
    playlists = []

    for playlist in api.PLAYLISTS:
        playlist.tracks = []
        playlists.append(playlist)

    return {"data": playlists}


@playlist_bp.route("/playlist/new", methods=["POST"])
def create_playlist():
    data = request.get_json()
    playlist = {"name": data["name"], "description": [], "tracks": []}

    try:
        p_in_db = instances.playlist_instance.get_playlist_by_name(playlist["name"])

        if p_in_db:
            raise Exception("Playlist already exists.")
    except Exception as e:
        return {"error": str(e)}, 409

    upsert_id = instances.playlist_instance.insert_playlist(playlist)
    p = instances.playlist_instance.get_playlist_by_id(upsert_id)

    api.PLAYLISTS.append(models.Playlist(p))

    return {"msg": "Playlist created successfully."}, 201


@playlist_bp.route("/playlist/<playlist_id>/add", methods=["POST"])
def add_track_to_playlist(playlist_id):
    data = request.get_json()

    pid = data["playlist"]
    trackid = data["track"]

    playlistlib.add_track(pid, trackid)
    return 200
