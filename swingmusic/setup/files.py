"""
This module contains the functions that are used to
create the config directory and copy the assets to the app directory.
"""

import shutil
from pathlib import Path

from swingmusic import settings
from swingmusic.utils.filesystem import get_home_res_path


def copy_assets_files():
    """
    Copies assets to the app directory.
    """

    # TODO: rework this file.
    #  Either import assets from inside the module, no need for copy
    #  or copy files with explicit location to config folder

    assets_dir = "assets"

    if settings.IS_BUILD:
        assets_dir = get_home_res_path("assets")

    src = Path(".").resolve() / assets_dir
    dest = (settings.Paths().app_dir / "assets").resolve()

    shutil.copytree(
        src,
        dest,
        ignore=shutil.ignore_patterns(
            "*.pyc",
        ),
        copy_function=shutil.copy2,
        dirs_exist_ok=True,
    )


def create_config_dir() -> None:
    """
    Creates the config directory if it doesn't exist.
    """
    # function kept for backward compatibility
    path = settings.Paths()
    # path.mkdir_config_folders() # will get executed on instantiation

    # copy assets to the app directory
    copy_assets_files()
