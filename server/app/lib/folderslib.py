from os import scandir
from typing import Dict, List
from typing import Set

from tqdm import tqdm

from app import api
from app import helpers
from app import models


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


def create_folder(foldername: str) -> models.Folder:
    """Create a single Folder object"""
    folder = {
        "name": foldername.split("/")[-1],
        "path": foldername,
        "trackcount": get_folder_track_count(foldername),
    }

    return models.Folder(folder)


def create_all_folders() -> Set[models.Folder]:
    folders: List[models.Folder] = []

    for foldername in tqdm(api.VALID_FOLDERS, desc="Creating folders"):
        folder = create_folder(foldername)
        folders.append(folder)

    return folders


def get_subdirs(foldername: str) -> List[models.Folder]:
    """
    Finds and Creates models.Folder objects for each sub-directory string in the foldername passed.
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
    folders_ = create_all_folders()
    """Create all the folder objects before clearing api.FOLDERS"""

    api.FOLDERS = folders_


class getFnF:
    def __init__(self, path: str) -> None:
        self.path = path

    @staticmethod
    def get_tracks(files: List[str]) -> List[models.Track]:
        """
        Returns a list of Track objects for each file in the given list.
        """
        return [file for file in api.TRACKS if file.filepath in files]

    def __call__(self) -> Dict[models.Track, models.Folder]:
        try:
            all = scandir(self.path)
        except FileNotFoundError:
            return ([], [])

        dirs, files = helpers.run_fast_scandir(self.path)

        tracks = self.get_tracks(files)
        folders = [create_folder(dir) for dir in dirs]

        return (tracks, folders)
