"""
All playlist-related routes.
"""
import json
from datetime import datetime

from flask import Blueprint, request
from PIL import UnidentifiedImageError

from app import models
from app.db.sqlite.playlists import SQLitePlaylistMethods
from app.lib import playlistlib
from app.utils.dates import date_string_to_time_passed, create_new_date
from app.utils.remove_duplicates import remove_duplicates

from app.store.tracks import TrackStore
from app.store.albums import AlbumStore

api = Blueprint("playlist", __name__, url_prefix="/")

PL = SQLitePlaylistMethods

insert_one_playlist = PL.insert_one_playlist
get_playlist_by_name = PL.get_playlist_by_name
count_playlist_by_name = PL.count_playlist_by_name
get_all_playlists = PL.get_all_playlists
get_playlist_by_id = PL.get_playlist_by_id
tracks_to_playlist = PL.add_tracks_to_playlist
add_artist_to_playlist = PL.add_artist_to_playlist
update_playlist = PL.update_playlist
delete_playlist = PL.delete_playlist


# get_tracks_by_trackhashes = SQLiteTrackMethods.get_tracks_by_trackhashes
def duplicate_images(images: list):
    if len(images) == 1:
        images *= 4
    elif len(images) == 2:
        images += list(reversed(images))
    elif len(images) == 3:
        images = images + images[:1]

    return images


def get_first_4_images(trackhashes: list[str]) -> list[dict['str', str]]:
    tracks = TrackStore.get_tracks_by_trackhashes(trackhashes)
    albums = []

    for track in tracks:
        if track.albumhash not in albums:
            albums.append(track.albumhash)
            if len(albums) == 4:
                break

    albums = AlbumStore.get_albums_by_hashes(albums)
    images = [
        {
            'image': album.image,
            'color': ''.join(album.colors),
        }
        for album in albums
    ]
    return duplicate_images(images)


@api.route("/playlists", methods=["GET"])
def send_all_playlists():
    """
    Gets all the playlists.
    """
    # get the no_images query param
    no_images = request.args.get("no_images", False)

    playlists = get_all_playlists()
    playlists = list(playlists)

    for playlist in playlists:
        if not no_images:
            playlist.images = get_first_4_images(playlist.trackhashes)
            playlist.images = [img['image'] for img in playlist.images]

        playlist.trackhashes = []
        playlist.artisthashes = []

    playlists.sort(
        key=lambda p: datetime.strptime(p.last_updated, "%Y-%m-%d %H:%M:%S"),
        reverse=True,
    )

    return {"data": playlists}


@api.route("/playlist/new", methods=["POST"])
def create_playlist():
    """
    Creates a new playlist. Accepts POST method with a JSON body.
    """
    data = request.get_json()

    if data is None:
        return {"error": "Playlist name not provided"}, 400

    existing_playlist_count = count_playlist_by_name(data["name"])

    if existing_playlist_count > 0:
        return {"error": "Playlist already exists"}, 409

    playlist = {
        "artisthashes": json.dumps([]),
        "banner_pos": 50,
        "has_gif": 0,
        "image": None,
        "last_updated": create_new_date(),
        "name": data["name"],
        "trackhashes": json.dumps([]),
    }

    playlist = insert_one_playlist(playlist)

    if playlist is None:
        return {"error": "Playlist could not be created"}, 500

    return {"playlist": playlist}, 201


@api.route("/playlist/<playlist_id>/add", methods=["POST"])
def add_track_to_playlist(playlist_id: str):
    """
    Takes a playlist ID and a track hash, and adds the track to the playlist
    """
    data = request.get_json()

    if data is None:
        return {"error": "Track hash not provided"}, 400

    trackhash = data["track"]

    insert_count = tracks_to_playlist(int(playlist_id), [trackhash])

    if insert_count == 0:
        return {"error": "Track already exists in playlist"}, 409

    add_artist_to_playlist(int(playlist_id), trackhash)
    PL.update_last_updated(int(playlist_id))

    return {"msg": "Done"}, 200


@api.route("/playlist/<playlistid>")
def get_playlist(playlistid: str):
    """
    Gets a playlist by id, and if it exists, it gets all the tracks in the playlist and returns them.
    """
    playlist = get_playlist_by_id(int(playlistid))

    if playlist is None:
        return {"msg": "Playlist not found"}, 404

    tracks = TrackStore.get_tracks_by_trackhashes(list(playlist.trackhashes))
    tracks = remove_duplicates(tracks)

    duration = sum(t.duration for t in tracks)
    playlist.last_updated = date_string_to_time_passed(playlist.last_updated)

    playlist.duration = duration

    if not playlist.has_image:
        playlist.images = get_first_4_images(playlist.trackhashes)

        if len(playlist.images) > 2:
            # swap 3rd image with first (3rd image is the visible image in UI)
            playlist.images[2], playlist.images[0] = playlist.images[0], playlist.images[2]

    playlist.trackhashes = []
    playlist.artisthashes = []

    return {"info": playlist, "tracks": tracks}


@api.route("/playlist/<playlistid>/update", methods=["PUT"])
def update_playlist_info(playlistid: str):
    if playlistid is None:
        return {"error": "Playlist ID not provided"}, 400

    db_playlist = get_playlist_by_id(int(playlistid))

    if db_playlist is None:
        return {"error": "Playlist not found"}, 404

    image = None

    if "image" in request.files:
        image = request.files["image"]

    data = request.form

    playlist = {
        "id": int(playlistid),
        "artisthashes": json.dumps([]),
        "banner_pos": db_playlist.banner_pos,
        "has_gif": 0,
        "image": db_playlist.image,
        "last_updated": create_new_date(),
        "name": str(data.get("name")).strip(),
        "trackhashes": json.dumps([]),
    }

    if image:
        try:
            playlist["image"] = playlistlib.save_p_image(image, playlistid)

            if image.content_type == "image/gif":
                playlist["has_gif"] = 1

            # reset banner position to center.
            playlist["banner_pos"] = 50
            PL.update_banner_pos(int(playlistid), 50)

        except UnidentifiedImageError:
            return {"error": "Failed: Invalid image"}, 400

    p_tuple = (*playlist.values(),)

    update_playlist(int(playlistid), playlist)

    playlist = models.Playlist(*p_tuple)
    playlist.last_updated = date_string_to_time_passed(playlist.last_updated)

    return {
        "data": playlist,
    }


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

    delete_playlist(pid)

    return {"msg": "Done"}, 200


@api.route("/playlist/<pid>/set-image-pos", methods=["POST"])
def update_image_position(pid: int):
    data = request.get_json()
    message = {"msg": "No data provided"}

    if data is None:
        return message, 400

    try:
        pos = data["pos"]
    except KeyError:
        return message, 400

    PL.update_banner_pos(pid, pos)

    return {"msg": "Image position saved"}, 200
