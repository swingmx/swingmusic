"""
Contains all the folder routes.
"""

import datetime
import os
from flask import Blueprint, request

from app import api
from app import settings
from app.lib import folderslib

folder_bp = Blueprint("folder", __name__, url_prefix="/")
from app import helpers


@folder_bp.route("/folder", methods=["POST"])
def get_folder_tree():
    """
    Returns a list of all the folders and tracks in the given folder.
    """
    data = request.get_json()
    req_dir = data["folder"]

    if req_dir == "$home":
        req_dir = settings.HOME_DIR

    folders = folderslib.get_subdirs(req_dir)
    songs = []

    for track in api.TRACKS:
        if track.folder == req_dir:
            songs.append(track)

    final_tracks = helpers.remove_duplicates(songs)

    return {
        "tracks": final_tracks,
        "folders": sorted(folders, key=lambda i: i.name),
    }
