"""
Contains all the folder routes.
"""

import os
from pathlib import Path

import psutil
from pydantic import BaseModel, Field
from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from showinfm import show_in_file_manager

from app import settings
from app.config import UserConfig
from app.db.libdata import TrackTable
from app.lib.folderslib import get_files_and_dirs, get_folders
from app.serializers.track import serialize_track
from app.utils.wintools import is_windows, win_replace_slash

tag = Tag(name="Folders", description="Get folders and tracks in a directory")
api = APIBlueprint("folder", __name__, url_prefix="/folder", abp_tags=[tag])


class FolderTree(BaseModel):
    folder: str = Field("$home", description="The folder to things from")
    sorttracksby: str = Field(
        "default",
        description="""The field to sort tracks by. Options: [
            "default",
            "album",
            "albumartists",
            "artists",
            "bitrate",
            "date",
            "disc",
            "duration",
            "last_mod",
            "lastplayed",
            "playduration",
            "playcount",
            "title",
        ]""",
    )
    tracksort_reverse: bool = Field(
        False,
        description="Whether to reverse the sort order of the tracks",
    )
    sortfoldersby: str = Field(
        "lastmod",
        description="""The field to sort folders by.
        Options: [
            "default",
            "name",
            "lastmod",
            "trackcount",
        ]
        """,
    )
    foldersort_reverse: bool = Field(
        False,
        description="Whether to reverse the sort order of the folders",
    )
    start: int = Field(0, description="The start index")
    limit: int = Field(50, description="The max number of items to return")
    tracks_only: bool = Field(False, description="Whether to only get tracks")


@api.post("")
def get_folder_tree(body: FolderTree):
    """
    Get folder

    Returns a list of all the folders and tracks in the given folder.
    """
    req_dir = body.folder
    tracks_only = body.tracks_only

    config = UserConfig()
    root_dirs = config.rootDirs

    try:
        if req_dir == "$home" and root_dirs[0] == "$home":
            req_dir = settings.Paths.USER_HOME_DIR
    except IndexError:
        pass

    if req_dir == "$home":
        if len(root_dirs) == 1:
            req_dir = root_dirs[0]
        else:
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
        req_dir = "/" + req_dir if not req_dir.startswith("/") else req_dir

    res = get_files_and_dirs(
        req_dir,
        start=body.start,
        limit=body.limit,
        tracks_only=tracks_only,
        tracksortby=body.sorttracksby,
        foldersortby=body.sortfoldersby,
        tracksort_reverse=body.tracksort_reverse,
        foldersort_reverse=body.foldersort_reverse,
    )

    return res


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


class DirBrowserBody(BaseModel):
    folder: str = Field(
        "$root",
        description="The folder to list directories from",
    )


@api.post("/dir-browser")
def list_folders(body: DirBrowserBody):
    """
    List folders

    Returns a list of all the folders in the given folder.
    Used when selecting root dirs.
    """
    req_dir = body.folder
    is_win = is_windows()

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


class FolderOpenInFileManagerQuery(BaseModel):
    path: str = Field(
        description="The path to open in the file manager",
    )


@api.get("/show-in-files")
def open_in_file_manager(query: FolderOpenInFileManagerQuery):
    """
    Open in file manager

    Opens the given path in the file manager on the host machine.
    """
    show_in_file_manager(query.path)

    return {"success": True}


class GetTracksInPathQuery(BaseModel):
    path: str = Field(
        description="The path to get tracks from",
    )


@api.get("/tracks/all")
def get_tracks_in_path(query: GetTracksInPathQuery):
    """
    Get tracks in path

    Gets all (or a max of 300) tracks from the given path and its subdirectories.

    Used when adding tracks to the queue.
    """
    tracks = TrackTable.get_tracks_in_path(query.path)
    tracks = (serialize_track(t) for t in tracks if Path(t.filepath).exists())

    return {
        "tracks": list(tracks)[:300],
    }
