"""
Contains all the track routes.
"""

import os
from pathlib import Path

from pydantic import BaseModel, Field
from flask_openapi3 import APIBlueprint, Tag
from flask import request, send_from_directory
from swingmusic.api.apischemas import TrackHashSchema
from swingmusic.config import UserConfig
from swingmusic.lib.trackslib import get_silence_paddings
from swingmusic.models.track import Track
from swingmusic.premium import TranscodeStream, transcoding_available

from swingmusic.store.tracks import TrackStore
from swingmusic.utils.files import guess_mime_type

bp_tag = Tag(name="File", description="Audio files")
api = APIBlueprint("track", __name__, url_prefix="/file", abp_tags=[bp_tag])

MP3_BITRATES = (96, 128, 192, 256, 320)


class SendTrackFileQuery(BaseModel):
    filepath: str = Field(description="The filepath to play (if available)")
    quality: str = Field(
        "original",
        description="The streaming bitrate in kbps. Options: original, 320, 256, 192, 128, 96",
    )


def validate_filepath(filepath: str):
    """
    Returns an error response if `filepath` is outside the root directories, else None.
    """
    # prevent path traversal
    if "/../" in filepath:
        return {"msg": "Invalid filepath", "error": "Path traversal detected"}, 400

    requested_filepath = Path(filepath).resolve()

    # check if filepath is a child of any of the root dirs
    for root_dir in UserConfig().rootDirs:
        if root_dir == "$home":
            root_dir = Path.home()
        else:
            root_dir = Path(root_dir).resolve()

        if root_dir in requested_filepath.parents:
            return None

    return {
        "msg": "Invalid filepath",
        "error": "File not inside root directories",
    }, 400


def find_track(trackhash: str, filepath: str) -> Track | None:
    """
    Returns the existing track at `filepath`, else the highest-bitrate existing track with `trackhash`.
    """
    tracks = TrackStore.get_tracks_by_filepaths([filepath])

    if len(tracks) > 0 and os.path.exists(tracks[0].filepath):
        for t in tracks:
            if os.path.exists(t.filepath) and t.trackhash == trackhash:
                return t

        return None

    group = TrackStore.trackhashmap.get(trackhash)

    # When finding by trackhash, sort by bitrate
    # and get the first track that exists
    if group is not None:
        for t in sorted(group.tracks, key=lambda x: x.bitrate, reverse=True):
            if os.path.exists(t.filepath):
                return t

    return None


def parse_quality(quality: str) -> int | None:
    """
    Returns the requested bitrate in kbps, or None for the original file. Raises ValueError on unsupported values.
    """
    quality = quality.strip().lower()
    if quality == "original":
        return None

    bitrate = int(quality)
    if bitrate not in MP3_BITRATES:
        raise ValueError(f"Unsupported bitrate: {bitrate}")

    return bitrate


def send_original(track: Track, as_attachment: bool = False):
    return send_from_directory(
        Path(track.filepath).parent,
        Path(track.filepath).name,
        mimetype=guess_mime_type(track.filepath),
        conditional=True,
        as_attachment=as_attachment,
    )


@api.get("/<trackhash>")
def send_track_file(path: TrackHashSchema, query: SendTrackFileQuery):
    """
    Get a playable audio file with Range support

    Returns the audio file for the given filepath, falling back to the track hash. With a `quality` bitrate below the source's and a premium license, streams an MP3 transcode instead.
    """
    trackhash = path.trackhash.strip()
    filepath = query.filepath.strip()

    error = validate_filepath(filepath)
    if error is not None:
        return error

    try:
        bitrate = parse_quality(query.quality)
    except ValueError:
        return {"msg": "Invalid quality"}, 400

    track = find_track(trackhash, filepath)
    if track is None:
        return {"msg": "File Not Found"}, 404

    if bitrate is not None and bitrate < track.bitrate:
        if transcoding_available() or (
            TranscodeStream is not None and TranscodeStream.has_session(track.trackhash, bitrate)
        ):
            return TranscodeStream.respond(track, bitrate, request.headers.get("Range"))

    return send_original(track)


@api.get("/<trackhash>/legacy")
def send_track_file_legacy(path: TrackHashSchema, query: SendTrackFileQuery):
    """
    Get a playable audio file without Range support

    Returns a playable audio file that corresponds to the given filepath. Falls back to track hash if filepath is not found.

    NOTE: Does not support range requests or transcoding.
    """
    filepath = query.filepath.strip()

    error = validate_filepath(filepath)
    if error is not None:
        return error

    track = find_track(path.trackhash.strip(), filepath)
    if track is None:
        return {"msg": "File Not Found"}, 404

    return send_original(track, as_attachment=True)


class GetAudioSilenceBody(BaseModel):
    ending_file: str = Field(description="The ending file's path")
    starting_file: str = Field(description="The beginning file's path")
    ending_trackhash: str = Field(description="The ending file's trackhash")
    starting_trackhash: str = Field(description="The beginning file's trackhash")


@api.post("/silence")
def get_audio_silence(body: GetAudioSilenceBody):
    """
    Get silence paddings

    Returns the duration of silence at the end of the current ending track and the duration of silence at the beginning of the next track.

    NOTE: Durations are in milliseconds.
    """
    ending_file = body.ending_file  # ending file's filepath
    starting_file = body.starting_file  # starting file's filepath

    if not TrackStore.is_valid_track_filepath(
        body.ending_trackhash, ending_file
    ) or not TrackStore.is_valid_track_filepath(
        body.starting_trackhash, starting_file
    ):
        return {"msg": "Invalid filepath"}, 400

    return get_silence_paddings(ending_file, starting_file)
