from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from pydantic import Field

from swingmusic.store.tracks import TrackStore
from swingmusic.api.apischemas import TrackHashSchema
from swingmusic.lib.lyrics import (
    get_lyrics_file,
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
    # 1. try to get lyrics by .lrc / .elrc file
    # 2. try to get lyrics by extra key
    # 3. try to get by duplicates
    # 4. iter plugins

    filepath = body.filepath
    trackhash = body.trackhash

    # get copyright first
    copyright = ""
    if entry:=TrackStore.trackhashmap.get(trackhash, None):
        for track in entry.tracks:
            copyright = track.copyright

            if copyright:
                break

    lyrics = get_lyrics_file(filepath)

    if not lyrics:
        lyrics = get_lyrics_from_tags(trackhash) # type: ignore

    if not lyrics:
        lyrics = get_lyrics_from_duplicates(filepath, trackhash)


    # check lyrics plugins

    if not lyrics:
        return {"error": "No lyrics found"}

    if lyrics.is_synced:
        text = lyrics.format_synced_lyrics()
    else:
        text = lyrics.format_unsynced_lyrics()

    return {"lyrics": text, "synced": lyrics.is_synced, "copyright": copyright}, 200


@api.post("/check")
def check_lyrics(body: SendLyricsBody):
    """
    Checks if lyrics file or tag exists for a track
    """
    result = send_lyrics(body)

    if "error" in result:
        return {"exists": False}
    else:
        return {"exists": True}, 200


