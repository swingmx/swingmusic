import os
from concurrent.futures import ThreadPoolExecutor

from app.db.store import Store
from app.logger import log
from app.models import Folder
from app.models import Track
from app.settings import SUPPORTED_FILES
from app.utils import win_replace_slash


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

        tracks = Store.get_tracks_by_filepaths(files)

        with ThreadPoolExecutor() as pool:
            iterable = pool.map(Store.get_folder, dirs)
            folders = [i for i in iterable if i is not None]

        folders = filter(lambda f: f.has_tracks, folders)

        return tracks, folders  # type: ignore
