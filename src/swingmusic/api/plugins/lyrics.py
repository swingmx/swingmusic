from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from pydantic import Field
from swingmusic.api.apischemas import TrackHashSchema
from swingmusic.lib.lyrics import format_synced_lyrics

from swingmusic.plugins.lyrics import Lyrics
from swingmusic.settings import Defaults
from swingmusic.utils.hashing import create_hash

bp_tag = Tag(name="Lyrics Plugin", description="Musixmatch lyrics plugin")
api = APIBlueprint(
    "lyricsplugin", __name__, url_prefix="/plugins/lyrics", abp_tags=[bp_tag]
)


class LyricsSearchBody(TrackHashSchema):
    title: str = Field(description="The track title ", example=Defaults.API_TRACKNAME)
    artist: str = Field(description="The track artist ", example=Defaults.API_ARTISTNAME)
    album: str = Field(description="The track track album ", example=Defaults.API_ALBUMNAME)
    filepath: str = Field(
        description="Track filepath to save the lyrics file relative to",
        example="/home/cwilvx/temp/crazy song.mp3",
    )


@api.post("/search")
def search_lyrics(body: LyricsSearchBody):
    """
    Search for lyrics by title and artist
    """
    title = body.title
    artist = body.artist
    album = body.album
    filepath = body.filepath
    trackhash = body.trackhash

    finder = Lyrics()
    data = finder.search_lyrics_by_title_and_artist(title, artist)

    if not data:
        return {"trackhash": trackhash, "lyrics": None}

    perfect_match = data[0]

    for track in data:
        i_title = track["title"]
        i_album = track["album"]

        if create_hash(i_title) == create_hash(title) and create_hash(
            i_album
        ) == create_hash(album):
            perfect_match = track

    track_id = perfect_match["track_id"]
    lrc = finder.download_lyrics(track_id, filepath)

    if lrc is not None:
        lines = lrc.split("\n")
        lyrics = format_synced_lyrics(lines)

        return {"trackhash": trackhash, "lyrics": lyrics}, 200

    return {"trackhash": trackhash, "lyrics": lrc}, 200
