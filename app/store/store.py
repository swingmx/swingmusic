"""
In memory store.
"""
from pathlib import Path

from tqdm import tqdm

from app.models import Folder
from app.utils.bisection import UseBisection
from app.utils.hashing import create_folder_hash
from app.utils.wintools import win_replace_slash
from .tracks import TrackStore


class FolderStore:
    """
    This class holds all tracks in memory and provides methods for
    interacting with them.
    """

    folders: list[Folder] = []

    @classmethod
    def check_has_tracks(cls, path: str):  # type: ignore
        """
        Checks if a folder has tracks.
        """
        path_hashes = "".join(f.path_hash for f in cls.folders)
        path_hash = create_folder_hash(*Path(path).parts[1:])

        return path_hash in path_hashes

    @classmethod
    def is_empty_folder(cls, path: str):
        """
        Checks if a folder has tracks using tracks in the store.
        """

        all_folders = set(track.folder for track in TrackStore.tracks)
        folder_hashes = "".join(
            create_folder_hash(*Path(f).parts[1:]) for f in all_folders
        )

        path_hash = create_folder_hash(*Path(path).parts[1:])
        return path_hash in folder_hashes

    @staticmethod
    def create_folder(path: str) -> Folder:
        """
        Creates a folder object from a path.
        """
        folder = Path(path)

        return Folder(
            name=folder.name,
            path=win_replace_slash(str(folder)),
            is_sym=folder.is_symlink(),
            has_tracks=True,
            path_hash=create_folder_hash(*folder.parts[1:]),
        )

    @classmethod
    def add_folder(cls, path: str):
        """
        Adds a folder to the store.
        """

        if cls.check_has_tracks(path):
            return

        folder = cls.create_folder(path)
        cls.folders.append(folder)

    @classmethod
    def remove_folder(cls, path: str):
        """
        Removes a folder from the store.
        """

        for folder in cls.folders:
            if folder.path == path:
                cls.folders.remove(folder)
                break

    @classmethod
    def process_folders(cls):
        """
        Creates a list of folders from the tracks in the store.
        """
        cls.folders.clear()

        all_folders = [track.folder for track in TrackStore.tracks]
        all_folders = set(all_folders)

        all_folders = [
            folder for folder in all_folders if not cls.check_has_tracks(folder)
        ]

        all_folders = [Path(f) for f in all_folders]
        # all_folders = [f for f in all_folders if f.exists()]

        valid_folders = []

        for folder in all_folders:
            try:
                if folder.exists():
                    valid_folders.append(folder)
            except PermissionError:
                pass

        for path in tqdm(valid_folders, desc="Processing folders"):
            folder = cls.create_folder(str(path))

            cls.folders.append(folder)

    @classmethod
    def get_folder(cls, path: str):  # type: ignore
        """
        Returns a folder object by its path.
        """
        # TODO: Modify this method to accept a list of paths, sorting is computationally expensive.
        folders = sorted(cls.folders, key=lambda x: x.path)
        folder = UseBisection(folders, "path", [path])()[0]

        if folder is not None:
            return folder

        has_tracks = cls.check_has_tracks(path)

        if not has_tracks:
            return None

        folder = cls.create_folder(path)
        cls.folders.append(folder)
        return folder

    @classmethod
    def get_folders_count(cls, paths: list[str]) -> list[dict[str, int]]:
        count_dict = {path: 0 for path in paths}

        for track in TrackStore.tracks:
            for path in paths:
                if track.filepath.startswith(path):
                    count_dict[path] += 1

        result = [{"path": path, "count": count_dict[path]} for path in paths]

        # TODO: Modify this method to return Folder objects with
        #   track count mapped. Keep an eye on function complexity.
        return result
