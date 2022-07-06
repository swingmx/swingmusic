"""
Contains the functions to prepare the server for use.
"""
import os
import shutil

from app import settings


class CopyFiles:
    """Copies assets to the app directory."""

    def __init__(self) -> None:
        files = [{
            "src": "assets",
            "dest": os.path.join(settings.APP_DIR, "assets"),
            "is_dir": True,
        }]

        for entry in files:
            src = os.path.join(os.getcwd(), entry["src"])

            if entry["is_dir"]:
                shutil.copytree(
                    src,
                    entry["dest"],
                    ignore=shutil.ignore_patterns("*.pyc", ),
                    copy_function=shutil.copy2,
                    dirs_exist_ok=True,
                )
                break

            shutil.copy2(src, entry["dest"])


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
        os.path.join("images", "playlists"),
    ]

    for _dir in dirs:
        path = os.path.join(config_folder, _dir)
        exists = os.path.exists(path)

        if not exists:
            os.makedirs(path)
            os.chmod(path, 0o755)

    CopyFiles()
