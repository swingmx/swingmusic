import os
from pathlib import Path
from importlib import resources as impresources
import swingmusic
from swingmusic.utils.wintools import win_replace_slash

CWD = Path(__file__).parent.resolve()

FILES = ["flac", "mp3", "wav", "m4a", "ogg", "wma", "opus", "alac", "aiff"]
SUPPORTED_FILES = tuple(f".{file}" for file in FILES)


def run_fast_scandir(_dir: str, full=False) -> tuple[list[str], list[str]]:
    """
    Scans a directory for files with a specific extension.
    Returns a list of files and folders in the directory.
    """
    # if on mac, ignore Library folder and its children
    if os.name == "posix":
        dir_path = Path(_dir)
        library_path = Path.home() / "Library"
        if dir_path == library_path or library_path in dir_path.parents:
            return [], []

    # if the path contains "node_modules" ignore
    if "node_modules" in _dir:
        return [], []

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
        return (impresources.files(swingmusic) / ".." / ".." / filename).resolve()
    except ValueError:
        return None
