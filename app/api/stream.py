"""
Contains all the track routes.
"""

import os
import time

from flask import Blueprint, send_file, request, Response
from flask_openapi3 import APIBlueprint, Tag
from pydantic import BaseModel, Field
from app.api.apischemas import TrackHashSchema
from app.lib.pydub.pydub.audio_segment import AudioSegment
from app.lib.trackslib import get_silence_paddings

from app.store.tracks import TrackStore
from app.utils.files import guess_mime_type

bp_tag = Tag(name="File", description="Audio files")
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

    # If filepath is provided, try to send that
    if filepath is not None:
        try:
            track = TrackStore.get_tracks_by_filepaths([filepath])[0]
        except IndexError:
            track = None

        track_exists = track is not None and os.path.exists(track.filepath)

        if track_exists:
            audio_type = guess_mime_type(filepath)
            return send_file_as_chunks(track.filepath, audio_type)

    # Else, find file by trackhash
    tracks = TrackStore.get_tracks_by_trackhashes([trackhash])

    for track in tracks:
        if track is None:
            return msg, 404

        audio_type = guess_mime_type(track.filepath)

        try:
            return send_file_as_chunks(track.filepath, audio_type)
        except (FileNotFoundError, OSError) as e:
            return msg, 404

    return msg, 404


def send_file_as_chunks(filepath: str, audio_type: str) -> Response:
    """
    Returns a Response object that streams the file in chunks.
    """
    # NOTE: +1 makes sure the last byte is included in the range.
    # NOTE: -1 is used to convert the end index to a 0-based index.
    chunk_size = 1024 * 360  # 360 KB

    # Get file size
    file_size = os.path.getsize(filepath)
    start = 0
    end = chunk_size

    # Read range header
    range_header = request.headers.get("Range")
    if range_header:
        start = get_start_range(range_header)

        # If start + chunk_size is greater than file_size,
        # set end to file_size - 1
        _end = start + chunk_size - 1

        if _end > file_size:
            end = file_size - 1
        else:
            end = _end

    def generate_chunks():
        with open(filepath, "rb") as file:
            file.seek(start)
            remaining_bytes = end - start + 1

            while remaining_bytes > 0:
                # Read the chunk size or all the remaining bytes
                chunk = file.read(min(chunk_size, remaining_bytes))
                yield chunk

                # Update the remaining bytes
                remaining_bytes -= len(chunk)

    response = Response(
        generate_chunks(),
        206,  # Partial Content status code
        mimetype=audio_type,
        content_type=audio_type,
        direct_passthrough=True,
    )
    response.headers.add("Content-Range", f"bytes {start}-{end}/{file_size}")
    response.headers.add("Accept-Ranges", "bytes")
    response.headers.add("Content-Length", str(end - start + 1))

    return response


def get_start_range(range_header: str):
    try:
        range_start, range_end = range_header.strip().split("=")[1].split("-")
        return int(range_start)

    except ValueError:
        return 0


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
