from flask import Blueprint
from app.store.albums import AlbumStore as Store

api = Blueprint("colors", __name__, url_prefix="/colors")


@api.route("/album/<albumhash>")
def get_album_color(albumhash: str):
    album = Store.get_album_by_hash(albumhash)

    msg = {"color": ""}

    if album is None or len(album.colors) == 0:
        return msg, 404

    return {"color": album.colors[0]}
