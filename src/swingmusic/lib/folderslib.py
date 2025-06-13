import os
from pathlib import Path

from swingmusic.lib.sortlib import sort_folders, sort_tracks
from swingmusic.logger import log
from swingmusic.models import Folder
from swingmusic.serializers.track import serialize_tracks
from swingmusic.utils.filesystem import SUPPORTED_FILES
from swingmusic.store.folder import FolderStore
from swingmusic.utils.wintools import win_replace_slash


def create_folder(path: str, trackcount=0) -> Folder:
    """
    Creates a folder object from a path.
    """
    folder = Path(path)

    return Folder(
        name=folder.name,
        path=win_replace_slash(str(folder)) + "/",
        is_sym=folder.is_symlink(),
        trackcount=trackcount,
    )


def get_folders(paths: list[str]):
    """
    Filters out folders that don't have any tracks and
    returns a list of folder objects.
    """
    folders = FolderStore.count_tracks_containing_paths(paths)
    return [
        create_folder(f["path"], f["trackcount"])
        for f in folders
        if f["trackcount"] > 0
    ]


def get_files_and_dirs(
    path: str,
    start: int,
    limit: int,
    tracksortby: str,
    foldersortby: str,
    tracksort_reverse: bool,
    foldersort_reverse: bool,
    tracks_only: bool = False,
    skip_empty_folders=True,
):
    """
    Given a path, returns a list of tracks and folders in that immediate path.

    Can recursively call itself to skip through empty folders.
    """
    # TODO: Replace os.path with pathlib
    try:
        entries = os.scandir(path)
    except FileNotFoundError:
        return {
            "path": path,
            "tracks": [],
            "folders": [],
        }

    dirs, files = [], []

    for entry_ in entries:
        entry = Path(entry_.path)
        ext = entry.suffix.lower()

        if entry.is_dir() and not entry.name.startswith("."):
            dir = (entry / "").as_posix()
            
            # add a trailing slash to the folder path
            # to avoid matching a folder starting with the same name as the root path
            # eg. .../Music and .../Music VideosI
            dirs.append(dir)
        elif entry.is_file() and ext in SUPPORTED_FILES:
            files.append(entry.as_posix())

    files_ = []

    for file in files:
        try:
            files_.append(
                {
                    "path": file,
                    "time": os.path.getmtime(file),
                }
            )
        except OSError as e:
            log.error(e)

    files_.sort(key=lambda f: f["time"])
    files = [f["path"] for f in files_]

    tracks = []
    if files:
        if limit == -1:
            limit = len(files)

        tracks = list(FolderStore.get_tracks_by_filepaths(files))
        tracks = sort_tracks(tracks, tracksortby, tracksort_reverse)
        tracks = tracks[start : start + limit]

    folders = []
    if not tracks_only:
        folders = get_folders(dirs)
        folders = sort_folders(folders, foldersortby, foldersort_reverse)

    if skip_empty_folders and len(folders) == 1 and len(tracks) == 0:
        # INFO: When we only have one folder and no tracks,
        # skip through empty folders.
        # Call recursively with the first folder in the list.
        return get_files_and_dirs(
            folders[0].path,
            start=start,
            limit=limit,
            tracksortby=tracksortby,
            foldersortby=foldersortby,
            tracksort_reverse=tracksort_reverse,
            foldersort_reverse=foldersort_reverse,
            tracks_only=tracks_only,
            skip_empty_folders=True,
        )

    return {
        "path": path,
        "tracks": serialize_tracks(tracks),
        "folders": folders,
        "total": len(files),
    }
