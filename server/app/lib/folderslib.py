from dataclasses import dataclass
from os import scandir
from typing import Tuple

from app.models import Folder
from app.models import Track

from app import instances


@dataclass
class Dir:
    path: str
    is_sym: bool


def get_folder_track_count(foldername: str) -> int:
    """
    Returns the number of files associated with a folder.
    """
    tracks = instances.tracks_instance.find_tracks_inside_path_regex(foldername)
    return len(tracks)


def create_folder(dir: Dir) -> Folder:
    """Create a single Folder object"""
    folder = {
        "name": dir.path.split("/")[-1],
        "path": dir.path,
        "is_sym": dir.is_sym,
        "trackcount": get_folder_track_count(dir.path),
    }

    return Folder(folder)


class getFnF:
    """
    Get files and folders from a directory.
    """

    def __init__(self, path: str) -> None:
        self.path = path

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
        tracks = instances.tracks_instance.find_songs_by_folder(self.path)
        tracks = [Track(track) for track in tracks]

        folders = [create_folder(dir) for dir in dirs]

        folders = filter(lambda f: f.trackcount > 0, folders)

        return tracks, folders
