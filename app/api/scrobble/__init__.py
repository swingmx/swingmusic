from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from pydantic import Field
from app.api.apischemas import TrackHashSchema

from app.db.libdata import AlbumTable, ArtistTable, TrackTable
from app.db.userdata import ScrobbleTable
from app.settings import Defaults

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

    track = TrackTable.get_track_by_trackhash(body.trackhash)

    if track is None:
        return {"msg": "Track not found."}, 404

    ScrobbleTable.add(dict(body))
    TrackTable.increment_playcount(body.trackhash, duration, timestamp)
    AlbumTable.increment_playcount(track.albumhash, duration, timestamp)
    ArtistTable.increment_playcount(track.artisthashes, duration, timestamp)

    return {"msg": "recorded"}, 201
