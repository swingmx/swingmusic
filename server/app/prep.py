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

    dirs = [
        "",
        "images",
        os.path.join("images", "artists"),
        os.path.join("images", "thumbnails"),
    ]

    for _dir in dirs:
        path = os.path.join(config_folder, _dir)

        try:
            os.path.exists(path)
        except FileNotFoundError:
            os.makedirs(path)
            os.chmod(path, 0o755)

        if _dir == dirs[3]:
            default_thumbnails_path = "../setup/default-images/thumbnails"

            try:
                os.path.exists(os.path.join(path, "defaults"))
            except FileNotFoundError:
                pass
