from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from pydantic import Field

from swingmusic.api.apischemas import TrackHashSchema
from swingmusic.lib.lyrics import (
    get_lyrics,
    check_lyrics_file,
    get_lyrics_from_duplicates,
    get_lyrics_from_tags,
)

bp_tag = Tag(name="Lyrics", description="Get lyrics")
api = APIBlueprint("lyrics", __name__, url_prefix="/lyrics", abp_tags=[bp_tag])


class SendLyricsBody(TrackHashSchema):
    filepath: str = Field(description="The path to the file")


@api.post("")
def send_lyrics(body: SendLyricsBody):
    """
    Returns the lyrics for a track
    """
    filepath = body.filepath
    trackhash = body.trackhash

    is_synced = True
    lyrics, copyright = get_lyrics(filepath, trackhash)

    if lyrics is None:
        lyrics, copyright = get_lyrics_from_duplicates(trackhash, filepath)

    if lyrics is None:
        lyrics, is_synced, copyright = get_lyrics_from_tags(trackhash) # type: ignore

    if lyrics is None:
        return {"error": "No lyrics found"}

    return {"lyrics": lyrics, "synced": is_synced, "copyright": copyright}, 200


@api.post("/check")
def check_lyrics(body: SendLyricsBody):
    """
    Checks if lyrics exist for a track
    """
    filepath = body.filepath
    trackhash = body.trackhash

    exists = check_lyrics_file(filepath, trackhash)

    if exists:
        return {"exists": exists}, 200

    exists = get_lyrics_from_tags(trackhash, just_check=True)

    return {"exists": exists}, 200
