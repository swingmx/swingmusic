import time
from typing import List
from typing import Set

from app import api
from app import helpers
from app import models
from progress.bar import Bar


def get_valid_folders() -> None:
    for track in api.TRACKS:
        api.VALID_FOLDERS.add(track.folder)


def get_folder_track_count(foldername: str) -> int:
    """
    Returns the number of files associated with a folder.
    """
    track_list = [track for track in api.TRACKS if foldername in track.folder]
    return len(track_list)


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
    _bar = Bar("Creating folders", max=len(api.VALID_FOLDERS))

    for foldername in api.VALID_FOLDERS:
        folder = create_folder(foldername)
        folders.append(folder)

        _bar.next()
    _bar.finish()

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
