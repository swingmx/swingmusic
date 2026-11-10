"""
Contains the classical music routes.
"""

from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from pydantic import BaseModel, Field

from swingmusic.premium import ClassicalStore, CloudError, LicenseError, classical_available

bp_tag = Tag(name="Classical", description="Classical works")
api = APIBlueprint("classical", __name__, url_prefix="/classical", abp_tags=[bp_tag])


class GetWorkPath(BaseModel):
    token: str = Field(
        description="A workhash or a catalogue id hash (catalogue_ids[].hash)",
    )


class GetWorkQuery(BaseModel):
    albumhash: str = Field(
        description="Focus the recording from this album (defaults to the recording with the most tracks)",
        default="",
    )


@api.get("/work/<token>")
def get_work(path: GetWorkPath, query: GetWorkQuery):
    """
    Get a classical work

    Returns the work's display data, the movements of the focused recording,
    and album cards for its other recordings. Resolves by workhash or by any
    of the work's catalogue id hashes (which survive re-indexing).

    Responds 404 when classical support is unavailable.
    """
    if not classical_available():
        return {"msg": "Work not found"}, 404

    try:
        work = ClassicalStore.get_work(path.token) or (
            ClassicalStore.get_work_by_catalogue_id(path.token)
        )

        if work is None:
            return {"msg": "Work not found"}, 404

        from swingmusic.premium.classical.serializers import serialize_work

        payload = serialize_work(work.workhash, albumhash=query.albumhash or None)

        if payload is None:
            return {"msg": "Work not found"}, 404

        return payload, 200
    except (LicenseError, CloudError, ImportError) as e:
        print("error serializing work", e)
        return {"msg": "Work not found"}, 404


def _classical_response(build, *args):
    """
    Run a classical home serializer, answering 404 when classical support is
    unavailable.
    """
    if not classical_available():
        return {"msg": "Classical support is off"}, 404
    try:
        return build(*args), 200
    except (LicenseError, CloudError, ImportError) as e:
        print("error serializing classical page", e)
        return {"msg": "Classical support is off"}, 404


class GetClassicalHomeQuery(BaseModel):
    card_limit: int = Field(default=10, ge=1, description="Album and composer cards to return")


@api.get("/home")
def get_classical_home(query: GetClassicalHomeQuery):
    """
    Get the classical home page

    Library counts, continue listening, albums, recently added, favorite
    works, composers, eras, instruments, work types, most played works, and
    performers, all from the user's library and listening.
    """
    from swingmusic.premium.classical.home import serialize_home

    return _classical_response(serialize_home, query.card_limit)


class GetClassicalWorksQuery(BaseModel):
    era: str = Field(default="", description="Era slug from the home page")
    instrument: str = Field(default="", description="Instrument slug from the home page")
    type: str = Field(default="", description="Work type slug from the home page")
    sort: str = Field(default="", description="added, favorites, or plays")


@api.get("/works")
def get_classical_works(query: GetClassicalWorksQuery):
    """
    Get classical works by era, instrument, or work type, or the recently
    added, favorite, or most played works
    """
    from swingmusic.premium.classical.home import serialize_works

    return _classical_response(
        serialize_works, query.era or None, query.instrument or None, query.type or None, query.sort or None
    )


class GetQueueWorksBody(BaseModel):
    trackhashes: list[str] = Field(description="Tracks added to the queue")


@api.post("/queue-works")
def get_queue_works(body: GetQueueWorksBody):
    """
    Get the works queued classical tracks belong to

    Each work carries the given tracks with their movement titles, so the
    queue can list them under it.
    """
    from swingmusic.premium.classical.serializers import serialize_queue_works

    return _classical_response(lambda: {"works": serialize_queue_works(body.trackhashes)})


@api.get("/composers")
def get_classical_composers():
    """
    Get every composer in the library as artist cards
    """
    from swingmusic.premium.classical.home import serialize_composers

    return _classical_response(serialize_composers)


@api.get("/albums")
def get_classical_albums():
    """
    Get every classical album in the library as album cards
    """
    from swingmusic.premium.classical.home import serialize_albums

    return _classical_response(serialize_albums)
