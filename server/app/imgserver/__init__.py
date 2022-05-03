from os import path
from typing import Tuple

from flask import Flask
from flask import send_from_directory

app = Flask(__name__)


def join(*args: Tuple[str]) -> str:
    return path.join(*args)


HOME = path.expanduser("~")
ROOT_PATH = path.join(HOME, ".alice", "images")

THUMB_PATH = join(ROOT_PATH, "thumbnails")
ARTIST_PATH = join(ROOT_PATH, "artists")
PLAYLIST_PATH = join(ROOT_PATH, "playlists")


@app.route("/")
def hello():
    return "Hello mf"


@app.route("/t/<imgpath>")
def send_thumbnail(imgpath: str):
    fpath = join(THUMB_PATH, imgpath)
    exists = path.exists(fpath)

    if exists:
        return send_from_directory(THUMB_PATH, imgpath)

    return {"msg": "Not found"}, 404


@app.route("/a/<imgpath>")
def send_artist_image(imgpath: str):
    print(ARTIST_PATH)
    fpath = join(ARTIST_PATH, imgpath)
    exists = path.exists(fpath)

    if exists:
        return send_from_directory(ARTIST_PATH, imgpath)

    return {"msg": "Not found"}, 404


@app.route('/p/<imgpath>')
def send_playlist_image(imgpath: str):
    fpath = join(PLAYLIST_PATH, imgpath)
    exists = path.exists(fpath)

    if exists:
        return send_from_directory(PLAYLIST_PATH, imgpath)

    return {"msg": "Not found"}, 404

# TODO
# Return Fallback images instead of JSON


if __name__ == "__main__":
    app.run(threaded=True, port=9877)
