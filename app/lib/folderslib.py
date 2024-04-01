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

    def get_files_and_dirs(self, path: str, skip_empty_folders=True):
        """
        Given a path, returns a list of tracks and folders in that immediate path.

        Can recursively call itself to skip through empty folders.
        """
        try:
            entries = os.scandir(path)
        except FileNotFoundError:
            return {
                "path": path,
                "tracks": [],
                "folders": [],
            }

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

        if skip_empty_folders and len(folders) == 1 and len(tracks) == 0:
            # INFO: When we only have one folder and no tracks,
            # skip through empty folders.
            # Call recursively with the first folder in the list.
            return self.get_files_and_dirs(folders[0].path)

        return {
            "path": path,
            "tracks": tracks,
            "folders": folders,
        }

    def __call__(self):
        return self.get_files_and_dirs(self.path)
