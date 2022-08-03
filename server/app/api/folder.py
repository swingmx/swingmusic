"""
Contains all the folder routes.
"""
from app import settings
from app.lib.folderslib import getFnF
from flask import Blueprint
from flask import request

folder_bp = Blueprint("folder", __name__, url_prefix="/")


@folder_bp.route("/folder", methods=["POST"])
def get_folder_tree():
    """
    Returns a list of all the folders and tracks in the given folder.
    """
    data = request.get_json()
    req_dir: str = data["folder"]

    if req_dir == "$home":
        req_dir = settings.HOME_DIR

    tracks, folders = getFnF(req_dir)()

    return {
        "tracks": tracks,
        "folders": sorted(folders, key=lambda i: i.name),
    }
