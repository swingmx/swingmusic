"""
Contains all the playlist routes.
"""
from datetime import datetime

from app import exceptions
from app import instances
from app import models
from app import serializer
from app.helpers import create_new_date
from app.helpers import Get
from app.helpers import UseBisection
from app.lib import playlistlib
from flask import Blueprint
from flask import request

playlist_bp = Blueprint("playlist", __name__, url_prefix="/")

PlaylistExists = exceptions.PlaylistExistsError
TrackExistsInPlaylist = exceptions.TrackExistsInPlaylistError


@playlist_bp.route("/playlists", methods=["GET"])
def get_all_playlists():
    """Returns all the playlists."""
    dbplaylists = instances.playlist_instance.get_all_playlists()
    dbplaylists = [models.Playlist(p) for p in dbplaylists]

    playlists = [
        serializer.Playlist(p, construct_last_updated=False) for p in dbplaylists
    ]
    playlists.sort(
        key=lambda p: datetime.strptime(p.lastUpdated, "%Y-%m-%d %H:%M:%S"),
        reverse=True,
    )
    return {"data": playlists}


@playlist_bp.route("/playlist/new", methods=["POST"])
def create_playlist():
    data = request.get_json()

    data = {
        "name": data["name"],
        "description": "",
        "pre_tracks": [],
        "lastUpdated": create_new_date(),
        "image": "",
        "thumb": "",
    }

    dbp = instances.playlist_instance.get_playlist_by_name(data["name"])

    if dbp is not None:
        return {"message": "Playlist already exists."}, 409

    upsert_id = instances.playlist_instance.insert_playlist(data)
    p = instances.playlist_instance.get_playlist_by_id(upsert_id)
    playlist = models.Playlist(p)

    return {"playlist": playlist}, 201


@playlist_bp.route("/playlist/<playlist_id>/add", methods=["POST"])
def add_track_to_playlist(playlist_id: str):
    data = request.get_json()

    trackid = data["track"]

    try:
        playlistlib.add_track(playlist_id, trackid)
    except TrackExistsInPlaylist:
        return {"error": "Track already exists in playlist"}, 409

    return {"msg": "I think It's done"}, 200


@playlist_bp.route("/playlist/<playlistid>")
def get_playlist(playlistid: str):
    p = instances.playlist_instance.get_playlist_by_id(playlistid)
    if p is None:
        return {"info": {}, "tracks": []}

    playlist = models.Playlist(p)

    tracks = playlistlib.create_playlist_tracks(playlist.pretracks)

    duration = sum([t.length for t in tracks])
    playlist = serializer.Playlist(playlist)
    playlist.duration = duration

    return {"info": playlist, "tracks": tracks}


@playlist_bp.route("/playlist/<playlistid>/update", methods=["PUT"])
def update_playlist(playlistid: str):
    image = None

    if "image" in request.files:
        image = request.files["image"]

    data = request.form

    playlist = {
        "name": str(data.get("name")).strip(),
        "description": str(data.get("description").strip()),
        "lastUpdated": create_new_date(),
        "image": None,
        "thumb": None,
    }

    playlists = Get.get_all_playlists()

    p = UseBisection(playlists, "playlistid", [playlistid])()
    p: models.Playlist = p[0]

    if playlist is not None:
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


@playlist_bp.route("/playlist/artists", methods=["POST"])
def get_playlist_artists():
    data = request.get_json()

    pid = data["pid"]
    artists = playlistlib.GetPlaylistArtists(pid)()

    return {"data": artists}
