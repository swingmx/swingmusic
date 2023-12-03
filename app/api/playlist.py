"""
All playlist-related routes.
"""
import json
from datetime import datetime
import pathlib

from flask import Blueprint, request
from PIL import UnidentifiedImageError, Image

from app import models
from app.db.sqlite.playlists import SQLitePlaylistMethods
from app.lib import playlistlib
from app.lib.albumslib import sort_by_track_no
from app.serializers.playlist import serialize_for_card
from app.store.tracks import TrackStore
from app.utils.dates import create_new_date, date_string_to_time_passed
from app.utils.remove_duplicates import remove_duplicates
from app.settings import Paths

api = Blueprint("playlist", __name__, url_prefix="/")

PL = SQLitePlaylistMethods


@api.route("/playlists", methods=["GET"])
def send_all_playlists():
    """
    Gets all the playlists.
    """
    no_images = request.args.get("no_images", False)

    playlists = PL.get_all_playlists()
    playlists = list(playlists)

    for playlist in playlists:
        if not no_images:
            playlist.images = playlistlib.get_first_4_images(
                trackhashes=playlist.trackhashes
            )
            playlist.images = [img["image"] for img in playlist.images]

        playlist.clear_lists()

    playlists.sort(
        key=lambda p: datetime.strptime(p.last_updated, "%Y-%m-%d %H:%M:%S"),
        reverse=True,
    )

    return {"data": playlists}


def insert_playlist(name: str, image: str = None):
    playlist = {
        "image": image,
        "last_updated": create_new_date(),
        "name": name,
        "trackhashes": json.dumps([]),
        "settings": json.dumps(
            {
                "has_gif": False,
                "banner_pos": 50,
                "square_img": True if image else False,
                "pinned": False,
            }
        ),
    }

    return PL.insert_one_playlist(playlist)


@api.route("/playlist/new", methods=["POST"])
def create_playlist():
    """
    Creates a new playlist. Accepts POST method with a JSON body.
    """
    data = request.get_json()

    if data is None:
        return {"error": "Playlist name not provided"}, 400

    existing_playlist_count = PL.count_playlist_by_name(data["name"])

    if existing_playlist_count > 0:
        return {"error": "Playlist already exists"}, 409

    playlist = insert_playlist(data["name"])

    if playlist is None:
        return {"error": "Playlist could not be created"}, 500

    return {"playlist": playlist}, 201


def get_path_trackhashes(path: str):
    """
    Returns a list of trackhashes in a folder.
    """
    tracks = TrackStore.get_tracks_in_path(path)
    tracks = sorted(tracks, key=lambda t: t.last_mod)
    return [t.trackhash for t in tracks]


def get_album_trackhashes(albumhash: str):
    """
    Returns a list of trackhashes in an album.
    """
    tracks = TrackStore.get_tracks_by_albumhash(albumhash)
    tracks = sort_by_track_no(tracks)

    return [t["trackhash"] for t in tracks]


def get_artist_trackhashes(artisthash: str):
    """
    Returns a list of trackhashes for an artist.
    """
    tracks = TrackStore.get_tracks_by_artisthash(artisthash)
    return [t.trackhash for t in tracks]


@api.route("/playlist/<playlist_id>/add", methods=["POST"])
def add_item_to_playlist(playlist_id: str):
    """
    Takes a playlist ID and a track hash, and adds the track to the playlist
    """
    data = request.get_json()

    if data is None:
        return {"error": "Track hash not provided"}, 400

    try:
        itemtype = data["itemtype"]
    except KeyError:
        itemtype = None

    try:
        itemhash: str = data["itemhash"]
    except KeyError:
        itemhash = None

    if itemtype == "tracks":
        trackhashes = itemhash.split(",")
    elif itemtype == "folder":
        trackhashes = get_path_trackhashes(itemhash)
    elif itemtype == "album":
        trackhashes = get_album_trackhashes(itemhash)
    elif itemtype == "artist":
        trackhashes = get_artist_trackhashes(itemhash)
    else:
        trackhashes = []

    insert_count = PL.add_tracks_to_playlist(int(playlist_id), trackhashes)

    if insert_count == 0:
        return {"error": "Item already exists in playlist"}, 409

    return {"msg": "Done"}, 200


@api.route("/playlist/<playlistid>")
def get_playlist(playlistid: str):
    """
    Gets a playlist by id, and if it exists, it gets all the tracks in the playlist and returns them.
    """
    no_tracks = request.args.get("no_tracks", "false")
    no_tracks = no_tracks == "true"

    is_recently_added = playlistid == "recentlyadded"

    if is_recently_added:
        playlist, tracks = playlistlib.get_recently_added_playlist()

        tracks = remove_duplicates(tracks)
        duration = sum(t.duration for t in tracks)

        playlist.set_duration(duration)
        playlist = serialize_for_card(playlist)

        return {"info": playlist, "tracks": tracks}

    playlist = PL.get_playlist_by_id(int(playlistid))

    if playlist is None:
        return {"msg": "Playlist not found"}, 404

    tracks = TrackStore.get_tracks_by_trackhashes(list(playlist.trackhashes))

    tracks = remove_duplicates(tracks)
    duration = sum(t.duration for t in tracks)
    playlist.last_updated = date_string_to_time_passed(playlist.last_updated)

    playlist.set_duration(duration)
    playlist.set_count(len(tracks))

    if not playlist.has_image:
        playlist.images = playlistlib.get_first_4_images(tracks)

    playlist.clear_lists()

    return {"info": playlist, "tracks": tracks if not no_tracks else []}


@api.route("/playlist/<playlistid>/update", methods=["PUT"])
def update_playlist_info(playlistid: str):
    if playlistid is None:
        return {"error": "Playlist ID not provided"}, 400

    db_playlist = PL.get_playlist_by_id(int(playlistid))

    if db_playlist is None:
        return {"error": "Playlist not found"}, 404

    image = None

    if "image" in request.files:
        image = request.files["image"]

    data = request.form

    settings = json.loads(data.get("settings"))
    settings["has_gif"] = False

    playlist = {
        "id": int(playlistid),
        "image": db_playlist.image,
        "last_updated": create_new_date(),
        "name": str(data.get("name")).strip(),
        "settings": settings,
        "trackhashes": json.dumps([]),
    }

    if image:
        try:
            pil_image = Image.open(image)
            content_type = image.content_type

            playlist["image"] = playlistlib.save_p_image(
                pil_image, playlistid, content_type
            )

            if image.content_type == "image/gif":
                playlist["settings"]["has_gif"] = True

        except UnidentifiedImageError:
            return {"error": "Failed: Invalid image"}, 400

    p_tuple = (*playlist.values(),)

    PL.update_playlist(int(playlistid), playlist)

    playlist = models.Playlist(*p_tuple)
    playlist.last_updated = date_string_to_time_passed(playlist.last_updated)

    return {
        "data": playlist,
    }


@api.route("/playlist/<playlistid>/pin_unpin", methods=["GET"])
def pin_unpin_playlist(playlistid: str):
    """
    Pins or unpins a playlist.
    """
    playlist = PL.get_playlist_by_id(int(playlistid))

    if playlist is None:
        return {"error": "Playlist not found"}, 404

    settings = playlist.settings

    try:
        settings["pinned"] = not settings["pinned"]
    except KeyError:
        settings["pinned"] = True

    PL.update_settings(int(playlistid), settings)

    return {"msg": "Done"}, 200


@api.route("/playlist/<playlistid>/remove-img", methods=["GET"])
def remove_playlist_image(playlistid: str):
    """
    Removes the playlist image.
    """
    pid = int(playlistid)
    playlist = PL.get_playlist_by_id(pid)

    if playlist is None:
        return {"error": "Playlist not found"}, 404

    PL.remove_banner(pid)

    playlist.image = None
    playlist.thumb = None
    playlist.settings["has_gif"] = False
    playlist.has_image = False

    playlist.images = playlistlib.get_first_4_images(trackhashes=playlist.trackhashes)
    playlist.last_updated = date_string_to_time_passed(playlist.last_updated)

    return {"playlist": playlist}, 200


@api.route("/playlist/delete", methods=["POST"])
def remove_playlist():
    """
    Deletes a playlist by ID.
    """
    message = {"error": "Playlist ID not provided"}
    data = request.get_json()

    if data is None:
        return message, 400

    try:
        pid = data["pid"]
    except KeyError:
        return message, 400

    PL.delete_playlist(pid)

    return {"msg": "Done"}, 200


@api.route("/playlist/<pid>/remove-tracks", methods=["POST"])
def remove_tracks_from_playlist(pid: int):
    data = request.get_json()

    if data is None:
        return {"error": "Track index not provided"}, 400

    # {
    #    trackhash: str;
    #    index: int;
    # }

    tracks = data["tracks"]
    PL.remove_tracks_from_playlist(pid, tracks)

    return {"msg": "Done"}, 200


def playlist_exists(name: str) -> bool:
    return PL.count_playlist_by_name(name) > 0


@api.route("/playlist/save-item", methods=["POST"])
def save_item_as_playlist():
    data = request.get_json()
    msg = {"error": "'itemtype', 'playlist_name' and 'itemhash' not provided"}, 400

    if data is None:
        return msg

    try:
        playlist_name = data["playlist_name"]
    except KeyError:
        playlist_name = None

    if playlist_exists(playlist_name):
        return {"error": "Playlist already exists"}, 409

    try:
        itemtype = data["itemtype"]
    except KeyError:
        itemtype = None

    try:
        itemhash: str = data["itemhash"]
    except KeyError:
        itemhash = None

    if itemtype is None or playlist_name is None or itemhash is None:
        return msg

    if itemtype == "tracks":
        trackhashes = itemhash.split(",")
    elif itemtype == "folder":
        trackhashes = get_path_trackhashes(itemhash)
    elif itemtype == "album":
        trackhashes = get_album_trackhashes(itemhash)
    elif itemtype == "artist":
        trackhashes = get_artist_trackhashes(itemhash)
    else:
        trackhashes = []

    if len(trackhashes) == 0:
        return {"error": "No tracks founds"}, 404

    image = (
        itemhash + ".webp" if itemtype != "folder" and itemtype != "tracks" else None
    )

    playlist = insert_playlist(playlist_name, image)

    if playlist is None:
        return {"error": "Playlist could not be created"}, 500

    # save image
    if itemtype != "folder" and itemtype != "tracks":
        filename = itemhash + ".webp"

        base_path = (
            Paths.get_artist_img_lg_path()
            if itemtype == "artist"
            else Paths.get_lg_thumb_path()
        )
        img_path = pathlib.Path(base_path + "/" + filename)

        if img_path.exists():
            img = Image.open(img_path)
            playlistlib.save_p_image(
                img, str(playlist.id), "image/webp", filename=filename
            )

    PL.add_tracks_to_playlist(playlist.id, trackhashes)
    playlist.set_count(len(trackhashes))

    images = playlistlib.get_first_4_images(trackhashes=trackhashes)
    playlist.images = [img["image"] for img in images]

    return {"playlist": playlist}, 201
