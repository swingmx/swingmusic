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
    fpath = join(THUMB_PATH, path)
    exists = os.path.exists(fpath)

    if exists:
        return send_from_directory(THUMB_PATH, path)

    return {"msg": "Not found"}, 404


@app.route("/artist/<path>")
def send_artist_image(path: str):
    print(ARTIST_PATH)
    fpath = join(ARTIST_PATH, path)
    exists = os.path.exists(fpath)

    if exists:
        return send_from_directory(ARTIST_PATH, path)

    return {"msg": "Not found"}, 404


if __name__ == "__main__":
    app.run(threaded=True, port=9877)
