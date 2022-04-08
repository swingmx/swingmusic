"""
Contains the functions to prepare the server for use.
"""
import os

from app import settings


def create_config_dir() -> None:
    """
    Creates the config directory if it doesn't exist.
    """

    _home_dir = os.path.expanduser("~")
    config_folder = os.path.join(_home_dir, settings.CONFIG_FOLDER)
    print(config_folder)

    dirs = [
        "",
        "images",
        os.path.join("images", "artists"),
        os.path.join("images", "thumbnails"),
        os.path.join("images", "playlists"),
    ]

    for _dir in dirs:
        path = os.path.join(config_folder, _dir)
        exists = os.path.exists(path)

        if not exists:
            os.makedirs(path)
            os.chmod(path, 0o755)
