from flask import Blueprint, request
from app import instances

playlist_bp = Blueprint("playlist", __name__, url_prefix="/")


@playlist_bp.route("/playlist/new")
def create_playlist():
    data = request.get_json()

    playlist = {
        "name": data["name"],
        "description": data["description"],
    }

    instances.playlist_instance.insert_playlist(playlist)
    return 200

@playlist_bp.route("/playlist/<playlist_id>")
def get_playlist(playlist_id):
    pass

@playlist_bp.route("/playlist/tracks/get", methods=["POST"])
def add_tracks_to_playlist():
    pass

@playlist_bp.route("/playlist/tracks/remove", methods=["POST"])
def remove_single_track():
    pass


@playlist_bp.route("/playlist/<playlist_id>/update/desc", methods=["POST"])
def update_playlist():
    pass

