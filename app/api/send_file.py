"""
Contains all the track routes.
"""

import os

from flask import Blueprint, send_file, request
from flask_openapi3 import APIBlueprint, Tag
from pydantic import BaseModel, Field
from app.api.apischemas import TrackHashSchema
from app.lib.trackslib import get_silence_paddings

from app.store.tracks import TrackStore

bp_tag = Tag(name="File", description="Single artist")
api = APIBlueprint("track", __name__, url_prefix="/file", abp_tags=[bp_tag])


class SendTrackFileQuery(BaseModel):
    filepath: str = Field(
        description="The filepath to play (if available)", default=None
    )


@api.get("/<trackhash>")
def send_track_file(path: TrackHashSchema, query: SendTrackFileQuery):
    """
    Get file

    Returns a playable audio file that corresponds to the given filepath. Falls back to track hash if filepath is not found.
    """
    trackhash = path.trackhash
    filepath = query.filepath
    msg = {"msg": "File Not Found"}

    def get_mime(filename: str) -> str:
        ext = filename.rsplit(".", maxsplit=1)[-1]
        return f"audio/{ext}"

    # If filepath is provide, try to send that
    if filepath is not None:
        try:
            track = TrackStore.get_tracks_by_filepaths([filepath])[0]
        except IndexError:
            track = None

        track_exists = track is not None and os.path.exists(track.filepath)

        if track_exists:
            audio_type = get_mime(filepath)
            return send_file(filepath, mimetype=audio_type)

    # Else, find file by trackhash
    tracks = TrackStore.get_tracks_by_trackhashes([trackhash])

    for track in tracks:
        if track is None:
            return msg, 404

        audio_type = get_mime(track.filepath)

        try:
            return send_file(track.filepath, mimetype=audio_type)
        except (FileNotFoundError, OSError) as e:
            return msg, 404

    return msg, 404


class GetAudioSilenceBody(BaseModel):
    ending_file: str = Field(
        description="The ending file's path",
        example="/home/cwilvx/Music/Made in Kenya/Sol generation/Bensoul - Salama.mp3",
    )
    starting_file: str = Field(
        description="The beginning file's path",
        example="/home/cwilvx/Music/Tidal/Albums/Bensoul - Qwarantunes/Bensoul - Peddi.m4a",
    )


@api.post("/silence")
def get_audio_silence(body: GetAudioSilenceBody):
    """
    Get silence paddings

    Returns the duration of silence at the end of the current ending track and the duration of silence at the beginning of the next track.

    NOTE: Durations are in milliseconds.
    """
    ending_file = body.ending_file  # ending file's filepath
    starting_file = body.starting_file  # starting file's filepath

    if ending_file is None or starting_file is None:
        return {"msg": "No filepath provided"}, 400

    return get_silence_paddings(ending_file, starting_file)
