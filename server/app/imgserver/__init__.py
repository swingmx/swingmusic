from os import path
from typing import Tuple

from flask import Flask
from flask import send_from_directory

app = Flask(__name__)


def join(*args: Tuple[str]) -> str:
    return path.join(*args)


HOME = path.expanduser("~")
APP_DIR = join(HOME, ".alice")
IMG_PATH = path.join(APP_DIR, "images")

ASSETS_PATH = join(APP_DIR, "assets")
THUMB_PATH = join(IMG_PATH, "thumbnails")
ARTIST_PATH = join(IMG_PATH, "artists")
PLAYLIST_PATH = join(IMG_PATH, "playlists")


@app.route("/")
def hello():
    return "Hello mf"


def send_fallback_img():
    img = join(ASSETS_PATH, "default.webp")
    exists = path.exists(img)

    if not exists:
        return "", 404

    return send_from_directory(ASSETS_PATH, "default.webp")


@app.route("/t/<imgpath>")
def send_thumbnail(imgpath: str):
    fpath = join(THUMB_PATH, imgpath)
    exists = path.exists(fpath)

    if exists:
        return send_from_directory(THUMB_PATH, imgpath)

    return send_fallback_img()


@app.route("/a/<imgpath>")
def send_artist_image(imgpath: str):
    fpath = join(ARTIST_PATH, imgpath)
    exists = path.exists(fpath)

    if exists:
        return send_from_directory(ARTIST_PATH, imgpath)

    return send_fallback_img()


@app.route("/p/<imgpath>")
def send_playlist_image(imgpath: str):
    fpath = join(PLAYLIST_PATH, imgpath)
    exists = path.exists(fpath)

    if exists:
        return send_from_directory(PLAYLIST_PATH, imgpath)

    return send_fallback_img()


if __name__ == "__main__":
    app.run(threaded=True, port=9877)
