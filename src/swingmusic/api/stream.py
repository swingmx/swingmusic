"""
Contains all the track routes.
"""

import os
from pathlib import Path
import tempfile
import time
from typing import Literal

from flask import send_file, request, Response, send_from_directory
from flask_openapi3 import APIBlueprint, Tag
from pydantic import BaseModel, Field
import werkzeug.wsgi
from swingmusic.api.apischemas import TrackHashSchema
from swingmusic.lib.trackslib import get_silence_paddings
from swingmusic.lib.transcoder import start_transcoding

from swingmusic.store.tracks import TrackStore
from swingmusic.utils.files import guess_mime_type

bp_tag = Tag(name="File", description="Audio files")
api = APIBlueprint("track", __name__, url_prefix="/file", abp_tags=[bp_tag])


class TransCodeStore:
    map: dict[str, str] = {}

    @classmethod
    def add_file(cls, trackhash: str, filepath: str):
        cls.map[trackhash] = filepath

    @classmethod
    def remove_file(cls, trackhash: str):
        del cls.map[trackhash]

    @classmethod
    def find(cls, trackhash: str):
        return cls.map.get(trackhash)


class SendTrackFileQuery(BaseModel):
    filepath: str = Field(description="The filepath to play (if available)")
    quality: str = Field(
        "original",
        description="The quality of the audio file. Options: original, 1411, 1024, 512, 320, 256, 128, 96",
    )
    container: Literal["mp3", "aac", "flac", "webm", "ogg"] = Field(
        "mp3",
        description="The container format of the audio file. Options: mp3, aac, flac, webm, ogg",
    )


@api.get("/<trackhash>/legacy")
def send_track_file_legacy(path: TrackHashSchema, query: SendTrackFileQuery):
    """
    Get a playable audio file without Range support

    Returns a playable audio file that corresponds to the given filepath. Falls back to track hash if filepath is not found.

    NOTE: Does not support range requests or transcoding.
    """
    trackhash = path.trackhash
    filepath = query.filepath
    msg = {"msg": "File Not Found"}

    track = None
    tracks = TrackStore.get_tracks_by_filepaths([filepath])

    if len(tracks) > 0 and os.path.exists(filepath):
        track = tracks[0]
    else:
        res = TrackStore.trackhashmap.get(trackhash)

        # When finding by trackhash, sort by bitrate
        # and get the first track that exists
        if res is not None:
            tracks = sorted(res.tracks, key=lambda x: x.bitrate, reverse=True)

            for t in tracks:
                if os.path.exists(t.filepath):
                    track = t
                    break

    if track is not None:
        audio_type = guess_mime_type(filepath)
        return send_from_directory(
            Path(filepath).parent,
            Path(filepath).name,
            mimetype=audio_type,
            conditional=True,
            as_attachment=True,
        )

    return msg, 404


@api.get("/<trackhash>")
def send_track_file(path: TrackHashSchema, query: SendTrackFileQuery):
    """
    Get a playable audio file with Range headers support

    Returns a playable audio file that corresponds to the given filepath. Falls back to track hash if filepath is not found.

    Transcoding can be done by sending the quality and container query parameters.

    **NOTES:**
    - Transcoded streams report incorrect duration during playback (idk why! FFMPEG gurus we need your help here).
    - The quality parameter is the desired bitrate in kbps.
    - The mp3 container is the best container for upto 320kbps (and has better duration reporting). The flac container allows for higher bitrates but it produces dramatically larger files (when transcoding from lossy formats).
    - You can get the transcoded bitrate by checking the X-Transcoded-Bitrate header on the first request's response.
    """
    trackhash = path.trackhash
    filepath = query.filepath

    # If filepath is provided, try to send that
    track = None
    tracks = TrackStore.get_tracks_by_filepaths([filepath])

    if len(tracks) > 0 and os.path.exists(filepath):
        track = tracks[0]
    else:
        res = TrackStore.trackhashmap.get(trackhash)

        # When finding by trackhash, sort by bitrate
        # and get the first track that exists
        if res is not None:
            tracks = sorted(res.tracks, key=lambda x: x.bitrate, reverse=True)

            for t in tracks:
                if os.path.exists(t.filepath):
                    track = t
                    break

    if track is not None:
        if query.quality == "original":
            return send_file_as_chunks(track.filepath)

        # prevent requesting over transcoding
        max_bitrate = track.bitrate
        requested_bitrate = int(query.quality)

        if query.container != "flac":
            # drop to 320 for non-flac containers
            requested_bitrate = min(320, requested_bitrate)

        quality = f"{min(max_bitrate, requested_bitrate)}k"
        return transcode_and_stream(trackhash, track.filepath, quality, query.container)

    return {"msg": "File Not Found"}, 404


def transcode_and_stream(trackhash: str, filepath: str, bitrate: str, container: str):
    """
    Initiates transcoding and returns the first chunk of the transcoded file.

    The other chunks are streamed on subsequent requests and are rerouted to `send_file_as_chunks`.
    """
    temp_file = TransCodeStore.find(trackhash)
    if temp_file is not None:
        return send_file_as_chunks(temp_file)

    format_params = {
        "mp3": ["-c:a", "libmp3lame"],
        "aac": ["-c:a", "aac"],
        "webm": ["-c:a", "libopus"],
        "ogg": ["-c:a", "libvorbis"],
        "flac": ["-c:a", "flac"],
        "wav": ["-c:a", "pcm_s16le"],
    }

    # Create a temporary file
    format = f".{container}" if container in format_params.keys() else ".flac"
    container_args = (
        format_params[container]
        if container in format_params.keys()
        else format_params["flac"]
    )
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=format)
    temp_filename = temp_file.name
    temp_file.close()

    TransCodeStore.add_file(trackhash, temp_filename)
    start_transcoding(filepath, temp_filename, bitrate, container_args)

    chunk_size = 1024 * 512  # 0.5MB
    file_size = os.path.getsize(filepath)

    def generate():
        # Poll for the output file
        while (
            not os.path.exists(temp_filename)
            or os.path.getsize(temp_filename) < chunk_size
        ):
            print(f"Waiting for transcoding to complete... filename: {temp_filename}")
            time.sleep(0.1)  # Wait for 100ms before checking again

        with open(temp_filename, "rb") as file:
            file.seek(0)
            return file.read(chunk_size)

    audio_type = guess_mime_type(temp_filename)
    response = Response(
        generate(),
        206,
        mimetype=audio_type,
        content_type=audio_type,
        direct_passthrough=True,
    )
    response.headers.add("Content-Range", f"bytes {0}-{chunk_size}/{file_size}")
    response.headers.add("Accept-Ranges", "bytes")
    response.headers.add("X-Transcoded-Bitrate", bitrate)
    return response


def send_file_as_chunks(filepath: str) -> Response:
    """
    Returns a Response object that streams the file in chunks.
    """
    # NOTE: +1 makes sure the last byte is included in the range.
    # NOTE: -1 is used to convert the end index to a 0-based index.
    chunk_size = 1024 * 512  # 0.5MB

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

            retry_count = 0
            max_retries = 10  # 5 * 100ms = 500ms total wait time

            while remaining_bytes > 0 or retry_count < max_retries:
                if retry_count == max_retries:
                    print("💚 sending final chunk! ...")

                    pos = file.tell()
                    chunk = file.read(os.path.getsize(filepath) - pos)

                    return chunk, pos, True

                if remaining_bytes < chunk_size:
                    time.sleep(0.25)
                    retry_count += 1
                    remaining_bytes = os.path.getsize(filepath) - file.tell()
                    continue

                chunk = file.read(min(chunk_size, remaining_bytes))
                if chunk:
                    remaining_bytes -= len(chunk)
                    return chunk, file.tell(), False
                else:
                    # If no data is read, wait for 100ms before retrying
                    time.sleep(0.25)
                    retry_count += 1

                    # update remaining bytes
                    remaining_bytes = os.path.getsize(filepath) - file.tell()
                    print(f"▶ Remaining bytes: {remaining_bytes}")

            return None, 0, True

    data, position, is_final = generate_chunks()

    audio_type = guess_mime_type(filepath)
    response = Response(
        response=data,
        status=206,  # Partial Content status code
        mimetype=audio_type,
        content_type=audio_type,
        direct_passthrough=True,
    )

    bytes_to_add = chunk_size if not is_final else 0
    response.headers.add(
        "Content-Range",
        f"bytes {start}-{position}/{os.path.getsize(filepath) + bytes_to_add}",
    )
    response.headers.add("Access-Control-Expose-Headers", "Content-Range")
    response.headers.add("Accept-Ranges", "bytes")
    return response


def get_start_range(range_header: str):
    try:
        range_start, range_end = range_header.strip().split("=")[1].split("-")
        return int(range_start)

    except ValueError:
        return 0


class GetAudioSilenceBody(BaseModel):
    ending_file: str = Field(description="The ending file's path")
    starting_file: str = Field(description="The beginning file's path")


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
