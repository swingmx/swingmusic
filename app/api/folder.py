"""
Contains all the folder routes.
"""
import os
from pathlib import Path

import psutil
from flask import Blueprint, request
from showinfm import show_in_file_manager

from app import settings
from app.db.sqlite.settings import SettingsSQLMethods as db
from app.lib.folderslib import GetFilesAndDirs, get_folders
from app.serializers.track import serialize_track
from app.store.tracks import TrackStore as store
from app.utils.wintools import is_windows, win_replace_slash

api = Blueprint("folder", __name__, url_prefix="")


@api.route("/folder", methods=["POST"])
def get_folder_tree():
    """
    Returns a list of all the folders and tracks in the given folder.
    """
    data = request.get_json()
    req_dir = "$home"

    tracks_only = False
    if data is not None:
        try:
            req_dir: str = data["folder"]
            tracks_only: bool = data["tracks_only"]
        except KeyError:
            req_dir = "$home"

    root_dirs = db.get_root_dirs()
    root_dirs.sort()

    try:
        if req_dir == "$home" and root_dirs[0] == "$home":
            req_dir = settings.Paths.USER_HOME_DIR
    except IndexError:
        pass

    if req_dir == "$home":
        folders = get_folders(root_dirs)

        return {
            "folders": folders,
            "tracks": [],
        }

    if is_windows():
        # Trailing slash needed when drive letters are passed,
        # Remember, the trailing slash is removed in the client.
        req_dir += "/"
    else:
        req_dir = "/" + req_dir + "/" if not req_dir.startswith("/") else req_dir + "/"

    tracks, folders = GetFilesAndDirs(req_dir, tracks_only=tracks_only)()

    return {
        "tracks": tracks,
        "folders": sorted(folders, key=lambda i: i.name),
    }


def get_all_drives(is_win: bool = False):
    """
    Returns a list of all the drives on a Windows machine.
    """
    drives = psutil.disk_partitions(all=True)
    drives = [d.mountpoint for d in drives]

    if is_win:
        drives = [win_replace_slash(d) for d in drives]
    else:
        remove = (
            "/boot",
            "/tmp",
            "/snap",
            "/var",
            "/sys",
            "/proc",
            "/etc",
            "/run",
            "/dev",
        )
        drives = [d for d in drives if not d.startswith(remove)]

    return drives


@api.route("/folder/dir-browser", methods=["POST"])
def list_folders():
    """
    Returns a list of all the folders in the given folder.
    """
    data = request.get_json()
    is_win = is_windows()

    try:
        req_dir: str = data["folder"]
    except KeyError:
        req_dir = "$root"

    if req_dir == "$root":
        return {
            "folders": [{"name": d, "path": d} for d in get_all_drives(is_win=is_win)]
        }

    if is_win:
        req_dir += "/"
    else:
        req_dir = "/" + req_dir + "/"
        req_dir = str(Path(req_dir).resolve())

    try:
        entries = os.scandir(req_dir)
    except PermissionError:
        return {"folders": []}

    dirs = [e.name for e in entries if e.is_dir() and not e.name.startswith(".")]
    dirs = [
        {"name": d, "path": win_replace_slash(os.path.join(req_dir, d))} for d in dirs
    ]

    return {
        "folders": sorted(dirs, key=lambda i: i["name"]),
    }


@api.route("/folder/show-in-files")
def open_in_file_manager():
    path = request.args.get("path")

    if path is None:
        return {"error": "No path provided."}, 400

    show_in_file_manager(path)

    return {"success": True}


@api.route("/folder/tracks/all")
def get_tracks_in_path():
    path = request.args.get("path")

    if path is None:
        return {"error": "No path provided."}, 400

    tracks = store.get_tracks_in_path(path)
    tracks = sorted(tracks, key=lambda i: i.last_mod)
    tracks = (serialize_track(t) for t in tracks if Path(t.filepath).exists())

    return {
        "tracks": list(tracks)[:300],
    }
