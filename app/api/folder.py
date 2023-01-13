"""
Contains all the folder routes.
"""
from flask import Blueprint, request

from app import settings
from app.lib.folderslib import GetFilesAndDirs

folderbp = Blueprint("folder", __name__, url_prefix="/")


@folderbp.route("/folder", methods=["POST"])
def get_folder_tree():
    """
    Returns a list of all the folders and tracks in the given folder.
    """
    data = request.get_json()

    if data is not None:
        req_dir: str = data["folder"]
    else:
        req_dir = settings.HOME_DIR

    if req_dir == "$home":
        req_dir = settings.HOME_DIR

    tracks, folders = GetFilesAndDirs(req_dir)()

    return {
        "tracks": tracks,
        "folders": sorted(folders, key=lambda i: i.name),
    }
