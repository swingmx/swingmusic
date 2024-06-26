"""
All playlist-related routes.
"""

import json
from datetime import datetime
import pathlib

from PIL import UnidentifiedImageError, Image
from pydantic import BaseModel, Field
from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint, FileStorage

from app import models
from app.db.sqlite.playlists import SQLitePlaylistMethods
from app.lib import playlistlib
from app.lib.albumslib import sort_by_track_no
from app.lib.home.recentlyadded import get_recently_added_playlist
from app.lib.home.recentlyplayed import get_recently_played_playlist
from app.serializers.playlist import serialize_for_card
from app.store.tracks import TrackStore
from app.utils.dates import create_new_date, date_string_to_time_passed
from app.utils.remove_duplicates import remove_duplicates
from app.settings import Paths

tag = Tag(name="Playlists", description="Get and manage playlists")
api = APIBlueprint("playlists", __name__, url_prefix="/playlists", abp_tags=[tag])

PL = SQLitePlaylistMethods


class SendAllPlaylistsQuery(BaseModel):
    no_images: bool = Field(False, description="Whether to include images")


@api.get("")
def send_all_playlists(query: SendAllPlaylistsQuery):
    """
    Gets all the playlists.
    """
    playlists = PL.get_all_playlists()
    playlists = list(playlists)

    for playlist in playlists:
        if not query.no_images:
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


class CreatePlaylistBody(BaseModel):
    name: str = Field(..., description="The name of the playlist")


@api.post("/new")
def create_playlist(body: CreatePlaylistBody):
    """
    New playlist

    Creates a new playlist. Accepts POST method with a JSON body.
    """
    existing_playlist_count = PL.count_playlist_by_name(body.name)

    if existing_playlist_count > 0:
        return {"error": "Playlist already exists"}, 409

    playlist = insert_playlist(body.name)

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


class PlaylistIDPath(BaseModel):
    # INFO: playlistid string examples: "recentlyadded"
    playlistid: int | str = Field(..., description="The ID of the playlist")


class AddItemToPlaylistBody(BaseModel):
    itemtype: str = Field(
        default="tracks",
        description="The type of item to add",
        examples=["tracks", "folder", "album", "artist"],
    )
    itemhash: str = Field(..., description="The hash of the item to add")


@api.post("/<playlistid>/add")
def add_item_to_playlist(path: PlaylistIDPath, body: AddItemToPlaylistBody):
    """
    Add to playlist.

    If itemtype is not "tracks", itemhash is expected to be a folder, album or artist hash.
    """
    itemtype = body.itemtype
    itemhash = body.itemhash
    playlist_id = path.playlistid

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


class GetPlaylistQuery(BaseModel):
    no_tracks: bool = Field(False, description="Whether to include tracks")


def format_custom_playlist(playlist: models.Playlist, tracks: list[models.Track]):
    duration = sum(t.duration for t in tracks)

    playlist.set_duration(duration)
    playlist = serialize_for_card(playlist)

    return {
        "info": playlist,
        "tracks": tracks,
    }


@api.get("/<playlistid>")
def get_playlist(path: PlaylistIDPath, query: GetPlaylistQuery):
    """
    Get playlist by id
    """
    no_tracks = query.no_tracks
    playlistid = path.playlistid

    custom_playlists = [
        {"name": "recentlyadded", "handler": get_recently_added_playlist},
        {"name": "recentlyplayed", "handler": get_recently_played_playlist},
    ]
    is_custom = playlistid in {p["name"] for p in custom_playlists}

    if is_custom:
        handler = next(
            p["handler"] for p in custom_playlists if p["name"] == playlistid
        )
        playlist, tracks = handler()
        return format_custom_playlist(playlist, tracks)

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


class UpdatePlaylistForm(BaseModel):
    image: FileStorage = Field(None, description="The image file")
    name: str = Field(..., description="The name of the playlist")
    settings: str = Field(
        ...,
        description="The settings of the playlist",
        example='{"has_gif": false, "banner_pos": 50, "square_img": false, "pinned": false}',
    )


@api.put("/<playlistid>/update", methods=["PUT"])
def update_playlist_info(path: PlaylistIDPath, form: UpdatePlaylistForm):
    """
    Update playlist
    """
    playlistid = path.playlistid
    db_playlist = PL.get_playlist_by_id(playlistid)

    if db_playlist is None:
        return {"error": "Playlist not found"}, 404

    image = form.image

    if form.image:
        image = form.image

    settings = json.loads(form.settings)
    settings["has_gif"] = False

    playlist = {
        "id": int(playlistid),
        "image": db_playlist.image,
        "last_updated": create_new_date(),
        "name": str(form.name).strip(),
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

    PL.update_playlist(playlistid, playlist)

    playlist = models.Playlist(*p_tuple)
    playlist.last_updated = date_string_to_time_passed(playlist.last_updated)

    return {
        "data": playlist,
    }


@api.post("/<playlistid>/pin_unpin")
def pin_unpin_playlist(path: PlaylistIDPath):
    """
    Pin playlist.
    """
    playlist = PL.get_playlist_by_id(path.playlistid)

    if playlist is None:
        return {"error": "Playlist not found"}, 404

    settings = playlist.settings

    try:
        settings["pinned"] = not settings["pinned"]
    except KeyError:
        settings["pinned"] = True

    PL.update_settings(path.playlistid, settings)

    return {"msg": "Done"}, 200


@api.delete("/<playlistid>/remove-img")
def remove_playlist_image(path: PlaylistIDPath):
    """
    Clear playlist image.
    """
    playlist = PL.get_playlist_by_id(path.playlistid)

    if playlist is None:
        return {"error": "Playlist not found"}, 404

    PL.remove_banner(path.playlistid)

    playlist.image = None
    playlist.thumb = None
    playlist.settings["has_gif"] = False
    playlist.has_image = False

    playlist.images = playlistlib.get_first_4_images(trackhashes=playlist.trackhashes)
    playlist.last_updated = date_string_to_time_passed(playlist.last_updated)

    return {"playlist": playlist}, 200


@api.delete("/<playlistid>/delete", methods=["DELETE"])
def remove_playlist(path: PlaylistIDPath):
    """
    Delete playlist
    """
    PL.delete_playlist(path.playlistid)

    return {"msg": "Done"}, 200


class RemoveTracksFromPlaylistBody(BaseModel):
    tracks: list[dict] = Field(..., description="A list of trackhashes to remove")


@api.post("/<playlistid>/remove-tracks")
def remove_tracks_from_playlist(
    path: PlaylistIDPath, body: RemoveTracksFromPlaylistBody
):
    """
    Remove track from playlist
    """
    # A track looks like this:
    # {
    #    trackhash: str;
    #    index: int;
    # }

    PL.remove_tracks_from_playlist(path.playlistid, body.tracks)

    return {"msg": "Done"}, 200


def playlist_name_exists(name: str) -> bool:
    return PL.count_playlist_by_name(name) > 0


class SavePlaylistAsItemBody(BaseModel):
    itemtype: str = Field(..., description="The type of item", example="tracks")
    playlist_name: str = Field(..., description="The name of the playlist")
    itemhash: str = Field(..., description="The hash of the item to save")


@api.post("/save-item")
def save_item_as_playlist(body: SavePlaylistAsItemBody):
    """
    Save as playlist

    Saves a track, album, artist or folder as a playlist
    """
    itemtype = body.itemtype
    playlist_name = body.playlist_name
    itemhash = body.itemhash

    if playlist_name_exists(playlist_name):
        return {"error": "Playlist already exists"}, 409

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
            Paths.get_lg_artist_img_path()
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
