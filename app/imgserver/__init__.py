import os
from pathlib import Path

from flask import Blueprint
from flask import request
from flask import send_from_directory

imgbp = Blueprint("imgserver", __name__, url_prefix="/img")
SUPPORTED_IMAGES = (".jpg", ".png", ".webp", ".jpeg")

HOME = os.path.expanduser("~")

APP_DIR = Path(HOME) / ".swing"
IMG_PATH = APP_DIR / "images"
ASSETS_PATH = APP_DIR / "assets"

THUMB_PATH = IMG_PATH / "thumbnails"
LG_THUMB_PATH = THUMB_PATH / "large"
SM_THUMB_PATH = THUMB_PATH / "small"

ARTIST_PATH = IMG_PATH / "artists"
ARTIST_LG_PATH = ARTIST_PATH / "large"
ARTIST_SM_PATH = ARTIST_PATH / "small"

PLAYLIST_PATH = IMG_PATH / "playlists"


@imgbp.route("/")
def hello():
    return "<h1>Image Server</h1>"


def send_fallback_img(filename: str = "default.webp"):
    img = ASSETS_PATH / filename

    if not img.exists():
        return "", 404

    return send_from_directory(ASSETS_PATH, filename)


@imgbp.route("/t/<imgpath>")
def send_lg_thumbnail(imgpath: str):
    fpath = LG_THUMB_PATH / imgpath

    if fpath.exists():
        return send_from_directory(LG_THUMB_PATH, imgpath)

    return send_fallback_img()


@imgbp.route("/t/s/<imgpath>")
def send_sm_thumbnail(imgpath: str):
    fpath = SM_THUMB_PATH / imgpath

    if fpath.exists():
        return send_from_directory(SM_THUMB_PATH, imgpath)

    return send_fallback_img()


@imgbp.route("/a/<imgpath>")
def send_lg_artist_image(imgpath: str):
    fpath = ARTIST_LG_PATH / imgpath

    if fpath.exists():
        return send_from_directory(ARTIST_LG_PATH, imgpath)

    return send_fallback_img("artist.webp")


@imgbp.route("/a/s/<imgpath>")
def send_sm_artist_image(imgpath: str):
    fpath = ARTIST_SM_PATH / imgpath

    if fpath.exists():
        return send_from_directory(ARTIST_SM_PATH, imgpath)

    return send_fallback_img("artist.webp")


@imgbp.route("/p/<imgpath>")
def send_playlist_image(imgpath: str):
    fpath = PLAYLIST_PATH / imgpath

    if fpath.exists():
        return send_from_directory(PLAYLIST_PATH, imgpath)

    return send_fallback_img("playlist.svg")


# @app.route("/raw")
# @app.route("/raw/<path:imgpath>")
# def send_from_filepath(imgpath: str = ""):
#     imgpath = "/" + imgpath
#     filename = path.basename(imgpath)

#     def verify_is_image():
#         _, ext = path.splitext(filename)
#         return ext in SUPPORTED_IMAGES

#     verified = verify_is_image()

#     if not verified:
#         return imgpath, 404

#     exists = path.exists(imgpath)

#     if verified and exists:
#         return send_from_directory(path.dirname(imgpath), filename)

#     return imgpath, 404

# def serve_imgs():
#     app.run(threaded=True, port=1971, host="0.0.0.0", debug=True)
