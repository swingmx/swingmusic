"""
All playlist-related routes.
"""

import csv
import json
import re
from datetime import datetime
from io import BytesIO, StringIO
import pathlib
from typing import Any

from flask import send_file
from PIL import UnidentifiedImageError, Image
from pydantic_core import core_schema
from pydantic import BaseModel, Field, GetCoreSchemaHandler

from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint, FileStorage as _FileStorage

from swingmusic import models
from swingmusic.api.apischemas import GenericLimitSchema
from swingmusic.db.userdata import PlaylistTable
from swingmusic.lib import playlistlib
from swingmusic.lib.albumslib import sort_by_track_no
from swingmusic.lib.home.recentlyadded import get_recently_added_playlist
from swingmusic.lib.home.recentlyplayed import get_recently_played_playlist
from swingmusic.lib.sortlib import sort_tracks
from swingmusic.models.playlist import Playlist
from swingmusic.serializers.playlist import serialize_for_card
from swingmusic.serializers.track import serialize_tracks

from swingmusic.store.tracks import TrackStore
from swingmusic.utils.dates import create_new_date, date_string_to_time_passed
from swingmusic.settings import Paths

tag = Tag(name="Playlists", description="Get and manage playlists")
api = APIBlueprint("playlists", __name__, url_prefix="/playlists", abp_tags=[tag])

PLAYLIST_SORT_KEYS = {
    "default",
    "album",
    "albumartists",
    "artists",
    "bitrate",
    "date",
    "disc",
    "duration",
    "last_mod",
    "lastplayed",
    "playduration",
    "playcount",
    "title",
    "filepath",
}


def normalize_sort_key(key: str | None) -> str:
    if key in PLAYLIST_SORT_KEYS:
        return key
    return "default"


def normalize_text(value: str) -> str:
    value = (value or "").casefold().strip()
    value = re.sub(r"\s+", " ", value)
    value = re.sub(r"[^\w\s]", "", value)
    return value


def get_track_isrc(track: models.Track) -> str:
    value = track.extra.get("isrc") or track.extra.get("ISRC")

    if isinstance(value, list):
        value = value[0] if value else ""

    return str(value or "").strip().upper()


def get_playlist_tracks(playlist: models.Playlist, sorttracksby: str, reverse: bool):
    tracks = TrackStore.get_tracks_by_trackhashes(playlist.trackhashes)
    sorttracksby = normalize_sort_key(sorttracksby)

    if sorttracksby != "default":
        tracks = sort_tracks(tracks, key=sorttracksby, reverse=reverse)

    return tracks


def slugify_filename(value: str) -> str:
    value = normalize_text(value).replace(" ", "_")
    return value or "playlist"


def build_spotify_match_index():
    exact_index: dict[tuple[str, str, tuple[str, ...]], models.Track] = {}
    soft_index: dict[tuple[str, tuple[str, ...]], models.Track] = {}
    title_index: dict[str, list[models.Track]] = {}
    isrc_index: dict[str, models.Track] = {}

    for track in TrackStore.get_flat_list():
        artists = tuple(sorted(normalize_text(a["name"]) for a in track.artists))
        exact_key = (
            normalize_text(track.title),
            normalize_text(track.album),
            artists,
        )
        soft_key = (normalize_text(track.title), artists)
        title_key = normalize_text(track.title)
        isrc = get_track_isrc(track)

        exact_index.setdefault(exact_key, track)
        soft_index.setdefault(soft_key, track)
        title_index.setdefault(title_key, []).append(track)

        if isrc:
            isrc_index.setdefault(isrc, track)

    return isrc_index, exact_index, soft_index, title_index


def match_spotify_row(
    row: dict[str, str],
    isrc_index: dict[str, models.Track],
    exact_index: dict[tuple[str, str, tuple[str, ...]], models.Track],
    soft_index: dict[tuple[str, tuple[str, ...]], models.Track],
    title_index: dict[str, list[models.Track]],
):
    spotify_isrc = str(row.get("ISRC") or "").strip().upper()
    track_name = normalize_text(row.get("Track Name", ""))
    album_name = normalize_text(row.get("Album Name", ""))
    artists = tuple(
        sorted(
            normalize_text(name)
            for name in str(row.get("Artist Name(s)", "")).split(",")
            if normalize_text(name)
        )
    )

    if spotify_isrc and spotify_isrc in isrc_index:
        return isrc_index[spotify_isrc], "isrc"

    exact_key = (track_name, album_name, artists)
    if exact_key in exact_index:
        return exact_index[exact_key], "exact"

    soft_key = (track_name, artists)
    if soft_key in soft_index:
        return soft_index[soft_key], "title_artists"

    for candidate in title_index.get(track_name, []):
        candidate_artists = {
            normalize_text(artist["name"]) for artist in candidate.artists
        }
        if candidate_artists.intersection(artists):
            return candidate, "title_overlap"

    return None, None


def insert_playlist(name: str, image: str = None):
    playlist = {
        "image": image,
        "last_updated": create_new_date(),
        "name": name,
        "trackhashes": [],
        "settings": {
            "has_gif": False,
            "banner_pos": 50,
            "square_img": True if image else False,
            "pinned": False,
        },
    }

    rowid = PlaylistTable.add_one(playlist)
    if rowid:
        playlist["id"] = rowid
        return Playlist(**playlist)

    return None


def get_path_trackhashes(path: str, tracksortby: str, reverse: bool):
    """
    Returns a list of trackhashes in a folder.
    """
    tracks = TrackStore.get_tracks_in_path(path)
    tracks = sort_tracks(tracks, key=tracksortby, reverse=reverse)
    return [t.trackhash for t in tracks]


def get_album_trackhashes(albumhash: str):
    """
    Returns a list of trackhashes in an album.
    """
    tracks = TrackStore.get_tracks_by_albumhash(albumhash)
    tracks = sort_by_track_no(tracks)

    return [t.trackhash for t in tracks]


def get_artist_trackhashes(artisthash: str):
    """
    Returns a list of trackhashes for an artist.
    """
    tracks = TrackStore.get_tracks_by_artisthash(artisthash)
    tracks = sort_tracks(tracks, key="playcount", reverse=True)
    return [t.trackhash for t in tracks]


def format_custom_playlist(playlist: models.Playlist, tracks: list[models.Track]):
    playlist.duration = sum(t.duration for t in tracks)
    playlist.count = len(tracks)

    return {
        "info": serialize_for_card(playlist),
        "tracks": serialize_tracks(tracks),
    }


class SendAllPlaylistsQuery(BaseModel):
    no_images: bool = Field(False, description="Whether to include images")


@api.get("")
def send_all_playlists(query: SendAllPlaylistsQuery):
    """
    Gets all the playlists.
    """
    playlists = PlaylistTable.get_all()
    playlists = sorted(
        playlists,
        key=lambda p: datetime.strptime(p.last_updated, "%Y-%m-%d %H:%M:%S"),
        reverse=True,
    )

    for playlist in playlists:
        if not playlist.has_image:
            playlist.images = playlistlib.get_first_4_images(
                trackhashes=playlist.trackhashes
            )

        playlist.clear_lists()

    # playlists.sort(
    #     key=lambda p: datetime.strptime(p.last_updated, "%Y-%m-%d %H:%M:%S"),
    #     reverse=True,
    # )

    return {"data": playlists}


class CreatePlaylistBody(BaseModel):
    name: str = Field(..., description="The name of the playlist")


@api.post("/new")
def create_playlist(body: CreatePlaylistBody):
    """
    New playlist

    Creates a new playlist. Accepts POST method with a JSON body.
    """
    exists = PlaylistTable.check_exists_by_name(body.name)

    if exists:
        return {"error": "Playlist already exists"}, 409

    playlist = insert_playlist(body.name)

    if playlist is None:
        return {"error": "Playlist could not be created"}, 500

    return {"playlist": playlist}, 201


class PlaylistIDPath(BaseModel):
    # INFO: playlistid string examples: "recentlyadded"
    playlistid: str = Field(..., description="The ID of the playlist")


class AddItemToPlaylistBody(BaseModel):
    itemtype: str = Field(
        default="tracks",
        description="The type of item to add",
        examples=["tracks", "folder", "album", "artist"],
    )
    sortoptions: dict = Field(
        default=None,
        description="The sort options for the tracks",
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
    playlist_id = int(path.playlistid)
    sortoptions = body.sortoptions

    if itemtype == "tracks":
        trackhashes = itemhash.split(",")
        if len(trackhashes) == 1 and trackhashes[0] in PlaylistTable.get_trackhashes(
            playlist_id
        ):
            return {"msg": "Track already exists in playlist"}, 409
    elif itemtype == "folder":
        trackhashes = get_path_trackhashes(
            itemhash,
            sortoptions.get("tracksortby") or "default",
            sortoptions.get("tracksortreverse") or False,
        )
    elif itemtype == "album":
        trackhashes = get_album_trackhashes(itemhash)
    elif itemtype == "artist":
        trackhashes = get_artist_trackhashes(itemhash)
    else:
        trackhashes = []

    PlaylistTable.append_to_playlist(playlist_id, trackhashes)
    return {"msg": "Done"}, 200


class GetPlaylistQuery(GenericLimitSchema):
    no_tracks: bool = Field(False, description="Whether to include tracks")
    start: int = Field(0, description="The start index of the tracks")
    sorttracksby: str = Field("default", description="How to sort playlist tracks")
    tracksort_reverse: bool = Field(
        False, description="Whether to reverse playlist track sort order"
    )


@api.get("/<playlistid>")
def get_playlist(path: PlaylistIDPath, query: GetPlaylistQuery):
    """
    Get playlist by id
    """
    no_tracks = query.no_tracks
    playlistid = path.playlistid
    sorttracksby = normalize_sort_key(query.sorttracksby)
    reverse = query.tracksort_reverse

    custom_playlists = [
        {"name": "recentlyadded", "handler": get_recently_added_playlist},
        {"name": "recentlyplayed", "handler": get_recently_played_playlist},
    ]
    is_custom = playlistid in {p["name"] for p in custom_playlists}

    if is_custom:
        if query.start != 0:
            return {
                "tracks": [],
            }

        handler = next(
            p["handler"] for p in custom_playlists if p["name"] == playlistid
        )
        playlist, tracks = handler()
        if sorttracksby != "default":
            tracks = sort_tracks(tracks, key=sorttracksby, reverse=reverse)
        return format_custom_playlist(playlist, tracks)

    playlist = PlaylistTable.get_by_id(int(playlistid))

    if playlist is None:
        return {"msg": "Playlist not found"}, 404

    all_tracks = get_playlist_tracks(playlist, sorttracksby, reverse)

    if query.limit == -1:
        tracks = all_tracks[query.start :]
    else:
        tracks = all_tracks[query.start : query.start + query.limit]

    duration = sum(t.duration for t in tracks)
    playlist._last_updated = date_string_to_time_passed(playlist.last_updated)
    playlist.duration = duration
    playlist.images = playlistlib.get_first_4_images(tracks)
    playlist.clear_lists()

    return {
        "info": playlist,
        "tracks": serialize_tracks(tracks) if not no_tracks else [],
    }


@api.get("/<playlistid>/export")
def export_playlist(path: PlaylistIDPath):
    """
    Export a playlist as CSV.
    """
    playlist = PlaylistTable.get_by_id(int(path.playlistid))

    if playlist is None:
        return {"error": "Playlist not found"}, 404

    tracks = get_playlist_tracks(playlist, "default", False)

    csv_buffer = StringIO()
    writer = csv.DictWriter(
        csv_buffer,
        fieldnames=[
            "Track Name",
            "Artist Name(s)",
            "Album Name",
            "Album Artist Name(s)",
            "Disc Number",
            "Track Number",
            "Track Duration (ms)",
            "File Path",
            "Track Hash",
        ],
    )
    writer.writeheader()

    for track in tracks:
        writer.writerow(
            {
                "Track Name": track.title,
                "Artist Name(s)": ", ".join(artist["name"] for artist in track.artists),
                "Album Name": track.album,
                "Album Artist Name(s)": ", ".join(
                    artist["name"] for artist in track.albumartists
                ),
                "Disc Number": track.disc,
                "Track Number": track.track,
                "Track Duration (ms)": track.duration,
                "File Path": track.filepath,
                "Track Hash": track.trackhash,
            }
        )

    payload = BytesIO(csv_buffer.getvalue().encode("utf-8"))
    payload.seek(0)

    return send_file(
        payload,
        mimetype="text/csv; charset=utf-8",
        as_attachment=True,
        download_name=f"{slugify_filename(playlist.name)}.csv",
    )


class FileStorage(_FileStorage):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.with_info_plain_validator_function(cls.validate)


class ImportSpotifyPlaylistForm(BaseModel):
    csv_file: FileStorage = Field(description="A Spotify playlist CSV export")


class UpdatePlaylistForm(BaseModel):
    image: FileStorage = Field(description="The image file")
    name: str = Field(..., description="The name of the playlist")
    settings: str = Field(
        ...,
        description="The settings of the playlist",
        json_schema_extra={
            "example": '{"has_gif": false, "banner_pos": 50, "square_img": false, "pinned": false}'
        },
    )


@api.put("/<playlistid>/update", methods=["PUT"])
def update_playlist_info(path: PlaylistIDPath, form: UpdatePlaylistForm):
    """
    Update playlist
    """
    playlistid = path.playlistid
    db_playlist = PlaylistTable.get_by_id(playlistid)

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

    PlaylistTable.update_one(playlistid, playlist)
    playlistlib.cleanup_playlist_images()

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
    playlist = PlaylistTable.get_by_id(path.playlistid)

    if playlist is None:
        return {"error": "Playlist not found"}, 404

    settings = playlist.settings

    try:
        settings["pinned"] = not settings["pinned"]
    except KeyError:
        settings["pinned"] = True

    PlaylistTable.update_settings(path.playlistid, settings)
    return {"msg": "Done"}, 200


@api.delete("/<playlistid>/remove-img")
def remove_playlist_image(path: PlaylistIDPath):
    """
    Clear playlist image.
    """
    playlist = PlaylistTable.get_by_id(path.playlistid)

    if playlist is None:
        return {"error": "Playlist not found"}, 404

    PlaylistTable.remove_image(path.playlistid)

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
    PlaylistTable.remove_one(path.playlistid)
    playlistlib.cleanup_playlist_images()
    return {"msg": "Done"}, 200


@api.post("/<playlistid>/import-spotify")
def import_spotify_playlist(path: PlaylistIDPath, form: ImportSpotifyPlaylistForm):
    """
    Import Spotify CSV rows into an existing playlist.
    """
    playlistid = int(path.playlistid)
    playlist = PlaylistTable.get_by_id(playlistid)

    if playlist is None:
        return {"error": "Playlist not found"}, 404

    try:
        csv_text = form.csv_file.stream.read().decode("utf-8-sig")
    except UnicodeDecodeError:
        return {"error": "CSV file must be UTF-8 encoded"}, 400

    rows = list(csv.DictReader(StringIO(csv_text)))
    if not rows:
        return {"error": "CSV file is empty"}, 400

    required_columns = {"Track Name", "Artist Name(s)"}
    if not required_columns.issubset(set(rows[0].keys())):
        return {"error": "Unsupported CSV format"}, 400

    isrc_index, exact_index, soft_index, title_index = build_spotify_match_index()
    matched_hashes: list[str] = []
    unmatched: list[dict[str, str]] = []
    matched_by: dict[str, int] = {
        "isrc": 0,
        "exact": 0,
        "title_artists": 0,
        "title_overlap": 0,
    }

    for row in rows:
        track, matched_on = match_spotify_row(
            row, isrc_index, exact_index, soft_index, title_index
        )

        if track is None:
            unmatched.append(
                {
                    "track": row.get("Track Name", ""),
                    "artists": row.get("Artist Name(s)", ""),
                    "album": row.get("Album Name", ""),
                }
            )
            continue

        matched_hashes.append(track.trackhash)
        if matched_on:
            matched_by[matched_on] += 1

    if not matched_hashes:
        return {
            "error": "No matching local tracks found in this CSV",
            "matched": 0,
            "rows": len(rows),
            "unmatched": unmatched[:25],
        }, 404

    before_hashes = PlaylistTable.get_trackhashes(playlistid) or []
    PlaylistTable.append_to_playlist(playlistid, matched_hashes)
    after_hashes = PlaylistTable.get_trackhashes(playlistid) or []
    added_count = len(after_hashes) - len(before_hashes)

    return {
        "msg": "Import complete",
        "rows": len(rows),
        "matched": len(matched_hashes),
        "added": added_count,
        "already_present": len(matched_hashes) - added_count,
        "unmatched": unmatched[:25],
        "matched_by": matched_by,
    }, 200


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

    PlaylistTable.remove_from_playlist(path.playlistid, body.tracks)

    return {"msg": "Done"}, 200


class SavePlaylistAsItemBody(BaseModel):
    itemtype: str = Field(..., description="The type of item", example="tracks")
    playlist_name: str = Field(..., description="The name of the playlist")
    itemhash: str = Field(..., description="The hash of the item to save")
    sortoptions: dict = Field(
        default=dict(),
        description="The sort options for the tracks",
    )


@api.post("/save-item")
def save_item_as_playlist(body: SavePlaylistAsItemBody):
    """
    Save as playlist

    Saves a track, album, artist or folder as a playlist
    """
    itemtype = body.itemtype
    playlist_name = body.playlist_name
    itemhash = body.itemhash
    sortoptions = body.sortoptions

    if PlaylistTable.check_exists_by_name(playlist_name):
        return {"error": "Playlist already exists"}, 409

    if itemtype == "tracks":
        trackhashes = itemhash.split(",")
    elif itemtype == "folder":
        trackhashes = get_path_trackhashes(
            itemhash,
            sortoptions.get("tracksortby") or "default",
            sortoptions.get("tracksortreverse") or False,
        )
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
            Paths().lg_artist_img_path
            if itemtype == "artist"
            else Paths().lg_thumb_path
        )
        img_path = pathlib.Path(base_path / filename)

        if img_path.exists():
            img = Image.open(img_path)
            playlistlib.save_p_image(
                img, str(playlist.id), "image/webp", filename=filename
            )

    PlaylistTable.append_to_playlist(playlist.id, trackhashes)
    playlist.count = len(trackhashes)

    images = playlistlib.get_first_4_images(trackhashes=trackhashes)
    playlist.images = [img["image"] for img in images]

    return {"playlist": playlist}, 201
