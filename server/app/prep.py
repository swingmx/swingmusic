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

    dirs = ["", "images", "images/artists", "images/thumbnails"]

    for _dir in dirs:
        path = os.path.join(config_folder, _dir)

        try:
            os.makedirs(path)
        except FileExistsError:
            pass

        os.chmod(path, 0o755)
