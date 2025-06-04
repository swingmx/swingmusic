"""
This module contains the functions that are used to
create the config directory and copy the assets to the app directory.
"""

import shutil
from pathlib import Path

from swingmusic import settings
from swingmusic.utils.filesystem import get_home_res_path


class CopyFiles:
    """
    Copies assets to the app directory.
    """

    def __init__(self) -> None:
        assets_dir = "assets"

        if settings.IS_BUILD:
            assets_dir = get_home_res_path("assets")

        files = [
            {
                "src": assets_dir,
                "dest": (settings.Paths.get_app_dir() / "assets").resolve(),
                "is_dir": True,
            }
        ]

        for entry in files:
            src = Path(".") / entry["src"]

            if entry["is_dir"]:
                shutil.copytree(
                    src,
                    entry["dest"],
                    ignore=shutil.ignore_patterns(
                        "*.pyc",
                    ),
                    copy_function=shutil.copy2,
                    dirs_exist_ok=True,
                )
                break

            shutil.copy2(src, entry["dest"])


def create_config_dir() -> None:
    """
    Creates the config directory if it doesn't exist.
    """
    # function kept for backward compatibility
    path = settings.Paths()
    # path.mkdir_config_folders() # will get executed on instantiation

    # copy assets to the app directory
    CopyFiles()
