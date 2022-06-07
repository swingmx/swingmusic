from dataclasses import dataclass
from os import scandir
from time import time
from typing import List
from typing import Set
from typing import Tuple

from app import api
from app import helpers
from app.models import Folder
from app.models import Track
from tqdm import tqdm


@dataclass
class Dir:
    path: str
    is_sym: bool


def get_valid_folders() -> None:
    for track in api.TRACKS:
        api.VALID_FOLDERS.add(track.folder)


def get_folder_track_count(foldername: str) -> int:
    """
    Returns the number of files associated with a folder.
    """
    count = 0
    for track in api.TRACKS:
        if foldername in track.folder:
            count += 1
    return count


def create_folder(dir: Dir) -> Folder:
    """Create a single Folder object"""
    folder = {
        "name": dir.path.split("/")[-1],
        "path": dir.path,
        "is_sym": dir.is_sym,
        "trackcount": get_folder_track_count(dir.path),
    }

    return Folder(folder)


def create_all_folders() -> Set[Folder]:
    folders: List[Folder] = []

    for foldername in tqdm(api.VALID_FOLDERS, desc="Creating folders"):
        folder = create_folder(foldername)
        folders.append(folder)

    return folders


def get_subdirs(foldername: str) -> List[Folder]:
    """
    Finds and Creates Folder objects for each sub-directory string in the foldername passed.
    """
    subdirs = set()

    for folder in api.VALID_FOLDERS:
        if foldername in folder:
            str0 = folder.replace(foldername, "")

            try:
                str1 = str0.split("/")[1]
            except IndexError:
                str1 = None

            if str1 is not None:
                subdirs.add(foldername + "/" + str1)
    return [create_folder(dir) for dir in subdirs]


@helpers.background
def run_scandir():
    """
    Initiates the creation of all folder objects for each folder with a track in it.

    Runs in a background thread after every 5 minutes.
    It calls the
    """
    get_valid_folders()
    # folders_ = create_all_folders()
    """Create all the folder objects before clearing api.FOLDERS"""

    # api.FOLDERS = folders_


class getFnF:
    """
    Get files and folders from a directory.
    """

    def __init__(self, path: str) -> None:
        self.path = path

    @classmethod
    def get_tracks(cls, files: List[str]) -> List[Track]:
        """
        Returns a list of Track objects for each file in the given list.
        """
        return helpers.UseBisection(api.TRACKS, "filepath", files)()

    def __call__(self) -> Tuple[Track, Folder]:
        try:
            all = scandir(self.path)
        except FileNotFoundError:
            return ([], [])

        dirs, files = [], []

        for entry in all:
            if entry.is_dir() and not entry.name.startswith("."):
                dir = {
                    "path": entry.path,
                    "is_sym": entry.is_symlink(),
                }
                dirs.append(Dir(**dir))
            elif entry.is_file() and entry.name.endswith((".mp3", ".flac")):
                files.append(entry.path)
        s = time()
        tracks = self.get_tracks(files)
        print(f"{time() - s} seconds to get tracks")

        folders = [create_folder(dir) for dir in dirs]
        folders = filter(lambda f: f.trackcount > 0, folders)

        return (tracks, folders)
