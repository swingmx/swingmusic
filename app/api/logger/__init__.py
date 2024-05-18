from flask_jwt_extended import current_user
from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from pydantic import Field
from app.api.apischemas import TrackHashSchema

from app.db.sqlite.logger.tracks import SQLiteTrackLogger as db
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
    trackhash = body.trackhash
    timestamp = body.timestamp
    duration = body.duration
    source = body.source

    if not timestamp or duration < 5:
        return {"msg": "Invalid entry."}, 400

    last_row = db.insert_track(
        trackhash=trackhash,
        timestamp=timestamp,
        duration=duration,
        source=source,
        userid=current_user["id"],
    )

    return {"total entries": last_row}
