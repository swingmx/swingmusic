import os
import pathlib
import sys
from pathlib import Path
import mimetypes

from swingmusic.settings import log
from swingmusic.utils import assets

FILES = ["flac", "mp3", "wav", "m4a", "ogg", "wma", "opus", "alac", "aiff"]
SUPPORTED_FILES = tuple(f".{file}" for file in FILES)

# TODO: Move this to config
# INFO: Skip these paths when scanning
IGNORE_PATH_ENDSWITH = {
    "node_modules",
    "site-packages",
    "postgres",
    "__pycache__",
    "/src",
    "/learnrs",
    "/venv",
    "/code",
    "/dist",
    "/demos",
    "/temp",
}

IGNORE_PATH_CONTAINS = {
    "Photos Library",
}


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

    if any(
        path.as_posix().endswith(ignore_path) for ignore_path in IGNORE_PATH_ENDSWITH
    ):
        return [], []

    if any(ignore_path in path.as_posix() for ignore_path in IGNORE_PATH_CONTAINS):
        return [], []

    # if on mac, ignore Library folder and its children
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
                    continue  # filter out system / hidden files
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

def guess_mime_type(filename: str) -> str:
    """
    Guess the mime type of file.

    :params filename: name of file
    :returns: 'audio/{guessed mime}'
    """
    mtype = mimetypes.guess_type(filename)[0]

    if mtype is None:
        ext = filename.rsplit(".", maxsplit=1)[-1]
        return f"audio/{ext}"

    return mtype

def validate_client_path(path:Path) -> bool:
    """
    Checks if there is an `index.html` file inside the provided path

    :args path: Path to static client folder.
    """

    path = Path(path)

    index = path / "index.html"
    return index.exists()


def get_default_config_path(path:Path=None) -> pathlib.Path:
    """
    Determines the default config path in the following order:

    1. Provided path - cli
    2. Env:``SWINGMUSIC_CONFIG_DIR`` - container
    3. Env:``xdg_config_home``
    4. <User Home>/.config
    5. <User Home>

    :args path: optional provided Path.
    :return: First valid path
    """

    container_config_dir = os.environ.get("SWINGMUSIC_CONFIG_DIR")
    xdg_config_home = os.environ.get("XDG_CONFIG_HOME")

    if path is not None:
        return path

    if container_config_dir is not None:
        return pathlib.Path(container_config_dir)

    if xdg_config_home is not None:
        return pathlib.Path(xdg_config_home)

    fallback_dir = pathlib.Path.home() / ".config"
    if fallback_dir.exists():
        return fallback_dir

    return pathlib.Path.home()

def get_default_client_path(config_path:Path) -> Path:
    """
    Determines the first valid client path.
    If always tries to use the provided path.
    If the path is empty, try downloading the client.
    On fail, switch to next path.

    1. container env provided client path - try download
    2. default client path (<config>/client) - try download
    3. fallback client path (<swingmusic>/client.zip) - will copy in default client path

    :args config_path: path to config
    :return: First valid path
    """


    env_client_dir = os.environ.get("SWINGMUSIC_CLIENT_DIR")
    default_config_path = config_path / "client"

    if env_client_dir is not None:
        env_client_dir = Path(env_client_dir)

        if env_client_dir.exists() and validate_client_path(env_client_dir):
            return env_client_dir
        else:
            env_client_dir.mkdir(parents=True, exist_ok=True)
            if assets.download_client_from_github(env_client_dir):
                return env_client_dir

    default_config_path.mkdir(parents=True, exist_ok=True)

    assets.download_client_from_github(default_config_path) or assets.extract_default_client(default_config_path)
    return default_config_path
