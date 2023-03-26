"""
This migration handles moving the config folder to the XDG standard location. 
It also handles moving the userdata and the downloaded artist images to the new location.
"""


import os
import shutil
from app.settings import Paths
from app.logger import log


class MoveToXdgFolder:
    version = 1
    name = "MoveToXdgFolder"

    @staticmethod
    def migrate():
        old_config_dir = os.path.join(Paths.USER_HOME_DIR, ".swing")
        new_config_dir = Paths.APP_DIR

        if not os.path.exists(old_config_dir):
            log.info("No old config folder found. Skipping migration.")
            return

        log.info("Found old config folder: %s", old_config_dir)
        old_imgs_dir = os.path.join(old_config_dir, "images")

        # move images to new location
        if os.path.exists(old_imgs_dir):
            shutil.copytree(
                old_imgs_dir,
                os.path.join(new_config_dir, "images"),
                copy_function=shutil.copy2,
                dirs_exist_ok=True,
            )

        log.warn("Moved artist images to: %s", new_config_dir)

        # move userdata.db to new location
        userdata_db = os.path.join(old_config_dir, "userdata.db")
        if os.path.exists(userdata_db):
            shutil.copy2(userdata_db, new_config_dir)

        log.warn("Moved userdata.db to: %s", new_config_dir)
        log.warn("Migration complete. ✅")

        # swing.db is not moved because the new code fixes bugs which require
        # the whole database to be recreated anyway. (ie. the bug which caused duplicate album and artist color entries)
