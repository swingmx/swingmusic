from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from pydantic import BaseModel, Field

from app.plugins.mixes import MixesPlugin
from app.store.homepage import HomepageStore
from app.store.tracks import TrackStore


bp_tag = Tag(name="Mixes Plugin", description="Mixes plugin hehe")
api = APIBlueprint(
    "mixesplugin", __name__, url_prefix="/plugins/mixes", abp_tags=[bp_tag]
)


@api.post("/track")
def get_track_mix():
    """
    Get a track mix
    """
    mixes = MixesPlugin()
    track = TrackStore.trackhashmap["9eeee292264ad01b"].get_best()
    tracks = mixes.get_track_mix([track])

    return {
        "total": len(tracks),
        "tracks": tracks,
    }


@api.post("/artist")
def get_artist_mix():
    mixes = MixesPlugin()
    # return mixes.create_artist_mixes()
    # tracks = mixes.get_artist_mix("09306be8039b98ad")

    # return {
    #     "total": len(tracks),
    #     "tracks": tracks,
    # }

    return "hi"


class MixQuery(BaseModel):
    mixid: str = Field(description="The mix id")


@api.get("/")
def get_mix(query: MixQuery):
    mixtype = ""

    match query.mixid[0]:
        case "a":
            mixtype = "artist_mixes"
        case _:
            return {"msg": "Invalid mix ID"}, 400

    mix = HomepageStore.get_mix(mixtype, query.mixid[1:])
    if mix:
        return mix, 200

    return {"msg": "Mix not found"}, 404
