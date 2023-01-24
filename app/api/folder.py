"""
Contains all the folder routes.
"""
import os

from pathlib import Path
from flask import Blueprint, request

from app import settings
from app.lib.folderslib import GetFilesAndDirs
from app.db.sqlite.settings import SettingsSQLMethods as db
from app.models import Folder
from app.utils import create_folder_hash

api = Blueprint("folder", __name__, url_prefix="/")


@api.route("/folder", methods=["POST"])
def get_folder_tree():
    """
    Returns a list of all the folders and tracks in the given folder.
    """
    data = request.get_json()

    if data is not None:
        try:
            req_dir: str = data["folder"]
        except KeyError:
            req_dir = "$home"

    root_dirs = db.get_root_dirs()

    try:
        if req_dir == "$home" and root_dirs[0] == "$home":
            req_dir = settings.USER_HOME_DIR
    except IndexError:
        pass

    if req_dir == "$home":
        folders = [Path(f) for f in root_dirs]

        return {
            "folders": [
                Folder(
                    name=f.name,
                    path=str(f),
                    has_tracks=True,
                    is_sym=f.is_symlink(),
                    path_hash=create_folder_hash(*f.parts[1:]),
                )
                for f in folders
            ],
            "tracks": [],
        }

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
