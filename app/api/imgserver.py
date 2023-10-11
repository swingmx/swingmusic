from pathlib import Path

from flask import Blueprint, send_from_directory

from app.settings import Paths

api = Blueprint("imgserver", __name__, url_prefix="/img")


@api.route("/")
def hello():
    return "<h1>Image Server</h1>"


def send_fallback_img(filename: str = "default.webp"):
    path = Paths.get_assets_path()
    img = Path(path) / filename

    if not img.exists():
        return "", 404

    return send_from_directory(path, filename)


@api.route("/t/o/<imgpath>")
def send_original_thumbnail(imgpath: str):
    path = Paths.get_original_thumb_path()
    fpath = Path(path) / imgpath

    if fpath.exists():
        return send_from_directory(path, imgpath)

    return send_fallback_img()


@api.route("/t/<imgpath>")
def send_lg_thumbnail(imgpath: str):
    path = Paths.get_lg_thumb_path()
    fpath = Path(path) / imgpath

    if fpath.exists():
        return send_from_directory(path, imgpath)

    return send_fallback_img()


@api.route("/t/s/<imgpath>")
def send_sm_thumbnail(imgpath: str):
    path = Paths.get_sm_thumb_path()
    fpath = Path(path) / imgpath

    if fpath.exists():
        return send_from_directory(path, imgpath)

    return send_fallback_img()


@api.route("/a/<imgpath>")
def send_lg_artist_image(imgpath: str):
    path = Paths.get_artist_img_lg_path()
    fpath = Path(path) / imgpath

    if fpath.exists():
        return send_from_directory(path, imgpath)

    return send_fallback_img("artist.webp")


@api.route("/a/s/<imgpath>")
def send_sm_artist_image(imgpath: str):
    path = Paths.get_artist_img_sm_path()
    fpath = Path(path) / imgpath

    if fpath.exists():
        return send_from_directory(path, imgpath)

    return send_fallback_img("artist.webp")


@api.route("/p/<imgpath>")
def send_playlist_image(imgpath: str):
    path = Paths.get_playlist_img_path()
    fpath = Path(path) / imgpath

    if fpath.exists():
        return send_from_directory(path, imgpath)

    return send_fallback_img("playlist.svg")
