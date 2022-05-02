import os
from typing import Tuple

from flask import Flask, send_from_directory

app = Flask(__name__)


def join(*args: Tuple[str]) -> str:
    return os.path.join(*args)


HOME = os.path.expanduser("~")
ROOT_PATH = os.path.join(HOME, ".alice", "images")

THUMB_PATH = join(ROOT_PATH, "thumbnails")
ARTIST_PATH = join(ROOT_PATH, "artists")


@app.route("/")
def hello():
    return "Hello mf"


@app.route("/thumb/<path>")
def send_thumbnail(path: str):
    name = path + ".webp"
    path = join(THUMB_PATH, name)
    exists = os.path.exists(path)

    if exists:
        return send_from_directory(THUMB_PATH, name)

    return {"msg": "Not found"}, 404


@app.route("/artist/<path>")
def send_artist_image(path: str):
    print(ARTIST_PATH)
    name = path + ".webp"
    path = join(ARTIST_PATH, name)
    exists = os.path.exists(path)

    if exists:
        return send_from_directory(ARTIST_PATH, name)

    return {"msg": "Not found"}, 404


if __name__ == "__main__":
    app.run(threaded=True, port=9877)
