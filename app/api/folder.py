"""
Contains all the folder routes.
"""
import os

from flask import Blueprint, request

from app import settings
from app.lib.folderslib import GetFilesAndDirs

api = Blueprint("folder", __name__, url_prefix="/")


@api.route("/folder", methods=["POST"])
def get_folder_tree():
    """
    Returns a list of all the folders and tracks in the given folder.
    """
    data = request.get_json()

    if data is not None:
        req_dir: str = data["folder"]
    else:
        req_dir = settings.USER_HOME_DIR

    if req_dir == "$home":
        req_dir = settings.USER_HOME_DIR

    tracks, folders = GetFilesAndDirs(req_dir)()

    return {
        "tracks": tracks,
        "folders": sorted(folders, key=lambda i: i.name),
    }


@api.route("/folder/dir-browser", methods=["POST"])
def list_folders():
    """
    Returns a list of all the folders in the given folder.
    """
    data = request.get_json()

    try:
        req_dir: str = data["folder"]
    except KeyError:
        req_dir = settings.USER_HOME_DIR

    if req_dir == "$home":
        req_dir = settings.USER_HOME_DIR

    entries = os.scandir(req_dir)

    dirs = [e.name for e in entries if e.is_dir() and not e.name.startswith(".")]
    dirs = [{"name": d, "path": os.path.join(req_dir, d)} for d in dirs]

    return {
        "folders": sorted(dirs, key=lambda i: i["name"]),
    }
