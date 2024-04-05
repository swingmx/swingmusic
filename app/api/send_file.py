"""
Contains all the track routes.
"""

import os

from flask import Blueprint, send_file, request, Response
from flask_openapi3 import APIBlueprint, Tag
from pydantic import BaseModel, Field
from app.api.apischemas import TrackHashSchema
from app.lib.trackslib import get_silence_paddings

from app.store.tracks import TrackStore

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

    def get_mime(filename: str) -> str:
        ext = filename.rsplit(".", maxsplit=1)[-1]
        return f"audio/{ext}"

    # If filepath is provided, try to send that
    if filepath is not None:
        try:
            track = TrackStore.get_tracks_by_filepaths([filepath])[0]
        except IndexError:
            track = None

        track_exists = track is not None and os.path.exists(track.filepath)

        if track_exists:
            audio_type = get_mime(filepath)
            return send_file_as_chunks(track.filepath, audio_type)

    # Else, find file by trackhash
    tracks = TrackStore.get_tracks_by_trackhashes([trackhash])

    for track in tracks:
        if track is None:
            return msg, 404

        audio_type = get_mime(track.filepath)

        try:
            return send_file_as_chunks(track.filepath, audio_type)
        except (FileNotFoundError, OSError) as e:
            return msg, 404

    return msg, 404


def send_file_as_chunks(filepath: str, audio_type: str) -> Response:
    file_size = os.path.getsize(filepath)
    start = 0
    end = file_size - 1

    range_header = request.headers.get("Range")
    if range_header:
        start, end = parse_range_header(range_header, file_size)

    chunk_size = 1024 * 1024  # 1MB chunk size (adjust as needed)

    def generate_chunks():
        with open(filepath, "rb") as file:
            file.seek(start)
            remaining_bytes = end - start + 1

            while remaining_bytes > 0:
                chunk = file.read(min(chunk_size, remaining_bytes))
                yield chunk
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


def parse_range_header(range_header: str, file_size: int) -> tuple[int, int]:
    try:
        range_start, range_end = range_header.strip().split("=")[1].split("-")
        start = int(range_start)
        end = min(int(range_end), file_size - 1)
    except ValueError:
        return 0, file_size - 1

    return start, end


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
