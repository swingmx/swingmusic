import os
from concurrent.futures import ThreadPoolExecutor

from app.models import Folder, Track
from app.settings import SUPPORTED_FILES
from app.logger import log
from app.utils.wintools import win_replace_slash

from app.store.store import FolderStore
from app.store.tracks import TrackStore


class GetFilesAndDirs:
    """
    Get files and folders from a directory.
    """

    def __init__(self, path: str) -> None:
        self.path = path

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

        # TODO: Remove this threadpool and modify the get_folder store
        #  method to accept a list of paths.
        with ThreadPoolExecutor() as pool:
            iterable = pool.map(FolderStore.get_folder, dirs)
            folders = [i for i in iterable if i is not None]

        folders = filter(lambda f: f.has_tracks, folders)

        # folders_with_count_dict = Store.get_folders_count(dirs)
        # pprint(folders_with_count_dict)
        # TODO: Map folder count to folder object

        return tracks, folders  # type: ignore
