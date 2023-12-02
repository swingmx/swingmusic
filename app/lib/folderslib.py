import os
from pathlib import Path

from app.logger import log
from app.models import Folder, Track
from app.settings import SUPPORTED_FILES
from app.utils.wintools import win_replace_slash

from app.store.tracks import TrackStore


def create_folder(path: str, count=0) -> Folder:
    """
    Creates a folder object from a path.
    """
    folder = Path(path)

    return Folder(
        name=folder.name,
        path=win_replace_slash(str(folder)),
        is_sym=folder.is_symlink(),
        count=count,
    )


def get_folders(paths: list[str]):
    """
    Filters out folders that don't have any tracks and
    returns a list of folder objects.
    """
    count_dict = {path: 0 for path in paths}

    for track in TrackStore.tracks:
        for path in paths:
            if track.folder.startswith(path):
                count_dict[path] += 1

    folders = [{"path": path, "count": count_dict[path]} for path in paths]
    return [create_folder(f["path"], f["count"]) for f in folders if f["count"] > 0]


class GetFilesAndDirs:
    """
    Get files and folders from a directory.
    """

    def __init__(self, path: str, tracks_only=False) -> None:
        self.path = path
        self.tracks_only = tracks_only

    def __call__(self) -> tuple[list[Track], list[Folder]]:
        try:
            entries = os.scandir(self.path)
        except FileNotFoundError:
            return [], []

        dirs, files = [], []

        for entry in entries:
            ext = os.path.splitext(entry.name)[1].lower()

            if entry.is_dir() and not entry.name.startswith("."):
                dirs.append(win_replace_slash(entry.path))
            elif entry.is_file() and ext in SUPPORTED_FILES:
                files.append(win_replace_slash(entry.path))

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

        tracks = TrackStore.get_tracks_by_filepaths(files)

        folders = []
        if not self.tracks_only:
            folders = get_folders(dirs)

        return tracks, folders
