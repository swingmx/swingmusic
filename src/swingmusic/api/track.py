"""
Contains the single-track metadata routes.
"""

import random

from flask_openapi3 import APIBlueprint, Tag
from pydantic import BaseModel, Field

from swingmusic.api.apischemas import TrackHashSchema
from swingmusic.serializers.track import serialize_track, serialize_tracks
from swingmusic.store.tracks import TrackStore

bp_tag = Tag(name="Track", description="Single track metadata")
# NOTE: blueprint name must differ from the "/file" blueprint, which is also
# named "track" internally.
api = APIBlueprint("trackmeta", __name__, url_prefix="/track", abp_tags=[bp_tag])


class GetTrackQuery(BaseModel):
    filepath: str = Field(
        "",
        description="Optional filepath to select a specific duplicate file "
        "indexed under this trackhash. Must belong to the trackhash.",
    )


class RandomTracksQuery(BaseModel):
    limit: int = Field(1000, ge=1, le=1000, description="How many tracks to return, at most 1000.")


@api.get("/random")
def get_random_tracks(query: RandomTracksQuery):
    """
    Get random tracks from the whole library

    Returns up to `limit` tracks in random order, one per trackhash.
    """
    groups = list(TrackStore.trackhashmap.values())
    picked = random.sample(groups, min(query.limit, len(groups)))
    return {"tracks": serialize_tracks([g.get_best() for g in picked])}


@api.get("/<trackhash>")
def get_track_by_hash(path: TrackHashSchema, query: GetTrackQuery):
    """
    Get a single track by its trackhash

    Returns the best (highest-bitrate) track for the trackhash. An optional
    `filepath` selects a specific duplicate file, which must belong to the
    trackhash.
    """
    trackhash = path.trackhash
    filepath = query.filepath

    # 404 if the trackhash is not indexed (None only happens for unknown hash)
    base = TrackStore.get_track(trackhash)
    if base is None:
        return {"error": "Track not found"}, 404

    if filepath:
        # the filepath must belong to this trackhash
        if not TrackStore.is_valid_track_filepath(trackhash, filepath):
            return {"error": "Invalid filepath"}, 400
        track = TrackStore.get_track(trackhash, filepath)
    else:
        track = base

    return serialize_track(track)
