import os
from flask import Blueprint

from app import api
from app import settings

folder_bp = Blueprint("folder", __name__, url_prefix="/")
from app import helpers


@folder_bp.route("/f/<folder>")
def get_folder_tree(folder: str):
    """
    Returns a list of all the folders and tracks in the given folder.
    """
    req_dir = folder.replace("|", "/")

    if folder == "home":
        req_dir = settings.HOME_DIR

    dir_content = os.scandir(os.path.join(settings.HOME_DIR, req_dir))

    folders = []
    files = []

    for entry in dir_content:
        if entry.is_dir() and not entry.name.startswith("."):
            files_in_dir = helpers.run_fast_scandir(entry.path, [".flac", ".mp3"])[1]

            if len(files_in_dir) != 0:
                _dir = {
                    "name": entry.name,
                    "count": len(files_in_dir),
                    "path": entry.path.replace(settings.HOME_DIR, ""),
                }

                folders.append(_dir)

        if entry.is_file():
            if entry.name.endswith(".flac") or entry.name.endswith(".mp3"):
                files.append(entry)

    files.sort(key=lambda x: os.path.getmtime(x.path))

    songs = []

    for entry in files:
        for track in api.TRACKS:
            if track.filepath == entry.path:
                songs.append(track)

    return {
        "files": helpers.remove_duplicates(songs),
        "folders": sorted(folders, key=lambda i: i["name"]),
    }
