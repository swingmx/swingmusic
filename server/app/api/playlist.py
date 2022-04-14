"""
Contains all the playlist routes.
"""
from datetime import datetime

from app import api
from app import exceptions
from app import instances
from app import models
from app import serializer
from app.lib import playlistlib
from flask import Blueprint
from flask import request

playlist_bp = Blueprint("playlist", __name__, url_prefix="/")

PlaylistExists = exceptions.PlaylistExists
TrackExistsInPlaylist = exceptions.TrackExistsInPlaylist


@playlist_bp.route("/playlists", methods=["GET"])
def get_all_playlists():
    playlists = [
        serializer.Playlist(p, construct_last_updated=False) for p in api.PLAYLISTS
    ]
    playlists.sort(
        key=lambda p: datetime.strptime(p.lastUpdated, "%Y-%m-%d %H:%M:%S"),
        reverse=True,
    )
    return {"data": playlists}


@playlist_bp.route("/playlist/new", methods=["POST"])
def create_playlist():
    data = request.get_json()

    playlist = {
        "name": data["name"],
        "description": "",
        "pre_tracks": [],
        "lastUpdated": data["lastUpdated"],
        "image": "",
        "thumb": "",
    }

    try:
        for pl in api.PLAYLISTS:
            if pl.name == playlist["name"]:
                raise PlaylistExists("Playlist already exists.")

    except PlaylistExists as e:
        return {"error": str(e)}, 409

    upsert_id = instances.playlist_instance.insert_playlist(playlist)
    p = instances.playlist_instance.get_playlist_by_id(upsert_id)
    pp = models.Playlist(p)

    api.PLAYLISTS.append(pp)

    return {"playlist": pp}, 201


@playlist_bp.route("/playlist/<playlist_id>/add", methods=["POST"])
def add_track_to_playlist(playlist_id: str):
    data = request.get_json()

    trackid = data["track"]

    try:
        playlistlib.add_track(playlist_id, trackid)
    except TrackExistsInPlaylist as e:
        return {"error": "Track already exists in playlist"}, 409

    return {"msg": "I think It's done"}, 200


@playlist_bp.route("/playlist/<playlistid>")
def get_single_p_info(playlistid: str):
    for p in api.PLAYLISTS:
        if p.playlistid == playlistid:
            tracks = p.get_tracks()
            return {
                "info": serializer.Playlist(p),
                "tracks": tracks,
            }

    return {"info": {}, "tracks": []}


@playlist_bp.route("/playlist/<playlistid>/update", methods=["PUT"])
def update_playlist(playlistid: str):
    image = None

    if "image" in request.files:
        image = request.files["image"]

    data = request.form

    playlist = {
        "name": str(data.get("name")).strip(),
        "description": str(data.get("description").strip()),
        "lastUpdated": str(data.get("lastUpdated")),
        "image": None,
        "thumb": None,
    }

    for p in api.PLAYLISTS:
        if p.playlistid == playlistid:

            if image:
                image_, thumb_ = playlistlib.save_p_image(image, playlistid)
                playlist["image"] = image_
                playlist["thumb"] = thumb_

            else:
                playlist["image"] = p.image.split("/")[-1]
                playlist["thumb"] = p.thumb.split("/")[-1]

            p.update_playlist(playlist)
            instances.playlist_instance.update_playlist(playlistid, playlist)

            return {
                "data": serializer.Playlist(p),
            }

    return {"msg": "Something shady happened"}, 500


# @playlist_bp.route("/playlist/<playlist_id>/info")
# def get_playlist_track(playlist_id: str):
#     tracks = playlistlib.get_playlist_tracks(playlist_id)
#     return {"data": tracks}
