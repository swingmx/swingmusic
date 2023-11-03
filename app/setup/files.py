"""
This module contains the functions that are used to
create the config directory and copy the assets to the app directory.
"""

import os
import shutil

from app import settings
from app.utils.filesystem import get_home_res_path


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
                "dest": os.path.join(settings.Paths.get_app_dir(), "assets"),
                "is_dir": True,
            }
        ]

        for entry in files:
            src = os.path.join(os.getcwd(), entry["src"])

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
    thumb_path = os.path.join("images", "thumbnails")
    small_thumb_path = os.path.join(thumb_path, "small")
    large_thumb_path = os.path.join(thumb_path, "large")
    original_thumb_path = os.path.join(thumb_path, "original")

    artist_img_path = os.path.join("images", "artists")
    small_artist_img_path = os.path.join(artist_img_path, "small")
    large_artist_img_path = os.path.join(artist_img_path, "large")

    playlist_img_path = os.path.join("images", "playlists")

    dirs = [
        "",  # creates the config folder
        "images",
        "plugins",
        "plugins/lyrics",
        thumb_path,
        small_thumb_path,
        large_thumb_path,
        original_thumb_path,
        artist_img_path,
        small_artist_img_path,
        large_artist_img_path,
        playlist_img_path,
    ]

    for _dir in dirs:
        path = os.path.join(settings.Paths.get_app_dir(), _dir)
        exists = os.path.exists(path)

        if not exists:
            os.makedirs(path)
            os.chmod(path, 0o755)

    CopyFiles()
