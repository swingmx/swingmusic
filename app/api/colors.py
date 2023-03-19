from flask import Blueprint
from app.db.store import Store

api = Blueprint("colors", __name__, url_prefix="/colors")


@api.route("/album/<albumhash>")
def get_album_color(albumhash: str):
    album = Store.get_album_by_hash(albumhash)

    return {
        "color": album.colors[0]
    }
