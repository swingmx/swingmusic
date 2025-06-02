"""
This module contains the functions that are used to
create the config directory and copy the assets to the app directory.
"""

import os
import shutil

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
    sm_thumb_path = settings.Paths.get_sm_thumb_path()
    lg_thumb_path = settings.Paths.get_lg_thumb_path()
    md_thumb_path = settings.Paths.get_md_thumb_path()
    xsm_thumb_path = settings.Paths.get_xsm_thumb_path()

    small_artist_img_path = settings.Paths.get_sm_artist_img_path()
    md_artist_img_path = settings.Paths.get_md_artist_img_path()
    large_artist_img_path = settings.Paths.get_lg_artist_img_path()

    playlist_img_path = os.path.join("images", "playlists")


    mixes_img_path = settings.Paths.get_mixes_img_path()
    og_mixes_img_path = settings.Paths.get_og_mixes_img_path()
    md_mixes_img_path = settings.Paths.get_md_mixes_img_path()
    sm_mixes_img_path = settings.Paths.get_sm_mixes_img_path()

    dirs = [
        "",  # creates the config folder
        sm_thumb_path,
        lg_thumb_path,
        md_thumb_path,
        xsm_thumb_path,
        "plugins/lyrics",
        playlist_img_path,
        md_artist_img_path,
        small_artist_img_path,
        large_artist_img_path,
        mixes_img_path,
        og_mixes_img_path,
        md_mixes_img_path,
        sm_mixes_img_path,
    ]

    for _dir in dirs:
        path = os.path.join(settings.Paths.get_app_dir(), _dir)
        exists = os.path.exists(path)

        if not exists:
            # exist_ok=True to create parent directories if they don't exist
            os.makedirs(path, exist_ok=True)
            os.chmod(path, 0o755)

    # copy assets to the app directory
    CopyFiles()
