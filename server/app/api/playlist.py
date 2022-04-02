"""
Contains all the playlist routes.
"""
from copy import deepcopy
from typing import List
from flask import Blueprint, request
from app import instances, api
from app.lib import playlistlib
from app import models
from app import exceptions

playlist_bp = Blueprint("playlist", __name__, url_prefix="/")

PlaylistExists = exceptions.PlaylistExists
TrackExistsInPlaylist = exceptions.TrackExistsInPlaylist


@playlist_bp.route("/playlists", methods=["GET"])
def get_all_playlists():
    ppp = deepcopy(api.PLAYLISTS)
    playlists = []

    for pl in ppp:
        pl.count = len(pl.tracks)
        pl.tracks = []
        playlists.append(pl)

    return {"data": playlists}


@playlist_bp.route("/playlist/new", methods=["POST"])
def create_playlist():
    data = request.get_json()

    playlist = {
        "name": data["name"],
        "description": "",
        "tracks": [],
        "count": 0,
        "lastUpdated": 0,
    }

    try:
        p_in_db = instances.playlist_instance.get_playlist_by_name(playlist["name"])

        if p_in_db:
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
        return {"error": str(e)}, 409

    return {"msg": "I think It's done"}, 200


@playlist_bp.route("/playlist/<playlist_id>")
def get_single_p_info(playlist_id: str):
    for p in api.PLAYLISTS:
        if p.playlistid == playlist_id:
            p.count = len(p.tracks)
            return {"data": p}


# @playlist_bp.route("/playlist/<playlist_id>/info")
# def get_playlist_track(playlist_id: str):
#     tracks = playlistlib.get_playlist_tracks(playlist_id)
#     return {"data": tracks}
