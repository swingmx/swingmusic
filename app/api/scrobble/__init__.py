from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from pydantic import Field
from app.api.apischemas import TrackHashSchema

from app.db.userdata import ScrobbleTable
from app.lib.extras import get_extra_info
from app.settings import Defaults
from app.store.albums import AlbumStore
from app.store.artists import ArtistStore
from app.store.tracks import TrackStore

bp_tag = Tag(name="Logger", description="Log item plays")
api = APIBlueprint("logger", __name__, url_prefix="/logger", abp_tags=[bp_tag])


class LogTrackBody(TrackHashSchema):
    timestamp: int = Field(description="The timestamp of the track", example=1622217600)
    duration: int = Field(
        description="The duration of the track in seconds", example=300
    )
    source: str = Field(
        description="The play source of the track",
        example=f"al:{Defaults.API_ALBUMHASH}",
    )


@api.post("/track/log")
def log_track(body: LogTrackBody):
    """
    Log a track play to the database.
    """
    timestamp = body.timestamp
    duration = body.duration

    if not timestamp or duration < 5:
        return {"msg": "Invalid entry."}, 400

    trackentry = TrackStore.trackhashmap.get(body.trackhash)
    if trackentry is None:
        return {"msg": "Track not found."}, 404

    scrobble_data = dict(body)
    scrobble_data["extra"] = get_extra_info(body.trackhash, "track")
    ScrobbleTable.add(scrobble_data)

    # Update play data on the in-memory stores
    track = trackentry.tracks[0]
    album = AlbumStore.albummap.get(track.albumhash)

    if album:
        album.increment_playcount(duration, timestamp)

    for hash in track.artisthashes:
        artist = ArtistStore.artistmap.get(hash)

        if artist:
            artist.increment_playcount(duration, timestamp)

    track = TrackStore.trackhashmap.get(body.trackhash)
    if track:
        track.increment_playcount(duration, timestamp)

    return {"msg": "recorded"}, 201
