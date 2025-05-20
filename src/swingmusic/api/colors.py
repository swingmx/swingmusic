from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from swingmusic.api.apischemas import AlbumHashSchema
from swingmusic.store.albums import AlbumStore as Store

bp_tag = Tag(name="Colors", description="Get item colors")
api = APIBlueprint("colors", __name__, url_prefix="/colors", abp_tags=[bp_tag])


@api.get("/album/<albumhash>")
def get_album_color(path: AlbumHashSchema):
    """
    Get album color
    """
    album = Store.get_album_by_hash(path.albumhash)

    msg = {"color": ""}

    if album is None or len(album.colors) == 0:
        return msg, 404

    return {"color": album.colors[0]}
