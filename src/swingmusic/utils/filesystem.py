import os
from pathlib import Path
import importlib.resources as imres


FILES = ["flac", "mp3", "wav", "m4a", "ogg", "wma", "opus", "alac", "aiff"]
SUPPORTED_FILES = tuple(f".{file}" for file in FILES)


def run_fast_scandir(path: str, full=False) -> tuple[list[str], list[str]]:
    """
    Scans a directory for files with a specific extension.
    Returns a list of files and folders in the directory.

    TODO: possible recursion error on link inside link: ``dir/folder1/subfolder1/<link-to-folder1>/subfolder1/...``

    :param path: folder to scan
    :param full: will call recursively until end of path.
    :return: (folder:[], files:[])
    """

    # filter out unwanted known folders
    if isinstance(path, str):
        if path == "":
            return [], []

    path = Path(path).resolve()

    if "node_modules" in path.as_posix():
        return [], []

    # if on mac, ignore Library folder and its children
    # TODO: test on real mac
    if os.name == "posix":
        library_path = (Path.home() / "Library").resolve()
        if path == library_path or str(path).startswith(str(library_path)):
            return [], []

    subfolders = []
    files = []

    try:
        for entry in path.iterdir():
            if entry.is_dir():
                if entry.name.startswith(".") or entry.name.startswith("$"):
                    continue # filter out system / hidden files
                else:
                    subfolders.append(entry)

            if entry.is_file():
                ext = entry.suffix.lower()
                if ext in SUPPORTED_FILES:
                    files.append(entry.as_posix())

        if full or len(files) == 0:
            for folder in subfolders:
                sub_dirs, subfiles = run_fast_scandir(folder, full=True)
                subfolders.extend(sub_dirs)
                files.extend(subfiles)

    except (OSError, PermissionError, FileNotFoundError, ValueError):
        return [], []

    return subfolders, files
