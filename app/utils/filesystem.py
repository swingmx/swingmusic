import os
from pathlib import Path

from app.settings import SUPPORTED_FILES
from app.utils.wintools import win_replace_slash

CWD = Path(__file__).parent.resolve()


def run_fast_scandir(_dir: str, full=False) -> tuple[list[str], list[str]]:
    """
    Scans a directory for files with a specific extension.
    Returns a list of files and folders in the directory.
    """

    if _dir == "":
        return [], []

    subfolders = []
    files = []

    try:
        for _file in os.scandir(_dir):
            if _file.is_dir() and not _file.name.startswith("."):
                subfolders.append(_file.path)
            if _file.is_file():
                ext = os.path.splitext(_file.name)[1].lower()
                if ext in SUPPORTED_FILES:
                    files.append(win_replace_slash(_file.path))

        if full or len(files) == 0:
            for _dir in list(subfolders):
                sub_dirs, _file = run_fast_scandir(_dir, full=True)
                subfolders.extend(sub_dirs)
                files.extend(_file)
    except (OSError, PermissionError, FileNotFoundError, ValueError):
        return [], []

    return subfolders, files


def get_home_res_path(filename: str):
    """
    Returns a path to resources in the home directory of this project.
    Used to resolve resources in builds.
    """
    try:
        return (CWD / ".." / ".." / filename).resolve()
    except ValueError:
        return None

def get_path_depth(path: str, strip_ext: bool=True):
    """
    If given a path "foo/bar/song.mp3"
    it will iterate and return their components:
    [
        'foo/bar/song.mp3',
        'bar/song.mp3',
        'song.mp3'
    ]
    """
    if strip_ext:
        path = os.path.splitext(path)[0]
    components = path.split('/')

    paths = []
    for i in range(len(components)):
        path = '/'.join(components[i:])
        paths.append(path)

    return paths[::-1]
