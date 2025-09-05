"""
This file contains all global variables.
All Variables should be read only after an initial set.

Contains default configs
"""

import logging
import pathlib
from pathlib import Path

from swingmusic.shared import Singleton, EnvStore

log = logging.getLogger(__name__)

class Paths(metaclass=Singleton):
    """
    This class stores all paths for ``swingmusic``s config.
    * Configs
    * DBs
    * Assets
    * Cache

    This class is a singleton.
    You cannot change the config path later.
    """

    config_parent: Path = Path.home().resolve()
    """
    The parent directory of the config folder.
    This is the directory where the config folder is located.
    """

    USER_HOME_DIR = Path.home().resolve()
    APP_DB_NAME = "swingmusic.db"
    USER_DATA_DB_NAME = "userdata.db"

    def __init__(self):
        """
        Create config-folder structure and check permissions.
        Copy all assets if needed.

        If `config` or `client` are provided, they are used exclusively.
        In the case of multithread, the environment vars are used.
        The detailed decision can be viewed in :func:`default_base_path`.

        :param self: Own object
        """

        store = EnvStore()
        self.config_parent = store["CONFIG_DIR"]
        self.client_path = store["CLIENT_DIR"]

    @property
    def config_folder_name(self) -> str:
        """
        return the name of the swingmusic config folder.

        When the base path is the same as the home dir,
        it returns `.swingmusic` else `swingmusic`
        """
        if self.config_parent == self.USER_HOME_DIR:
            return ".swingmusic"
        else:
            return "swingmusic"

    @property
    def config_dir(self) -> Path:
        return self.config_parent / self.config_folder_name

    @property
    def img_path(self) -> Path:
        return self.config_dir / "images"

    # ARTISTS
    @property
    def artist_img_path(self) -> Path:
        return self.img_path / "artists"

    @property
    def sm_artist_img_path(self) -> Path:
        return self.artist_img_path / "small"

    @property
    def md_artist_img_path(self) -> pathlib.Path:
        return self.artist_img_path / "medium"

    @property
    def lg_artist_img_path(self) -> pathlib.Path:
        return self.artist_img_path / "large"

    # TRACK THUMBNAILS
    @property
    def thumbs_path(self) -> pathlib.Path:
        return self.img_path / "thumbnails"

    @property
    def sm_thumb_path(self) -> pathlib.Path:
        return self.thumbs_path / "small"

    @property
    def xsm_thumb_path(self) -> pathlib.Path:
        return self.thumbs_path / "xsmall"

    @property
    def md_thumb_path(self) -> pathlib.Path:
        return self.thumbs_path / "medium"

    @property
    def lg_thumb_path(self) -> pathlib.Path:
        return self.thumbs_path / "large"

    # OTHERS
    @property
    def playlist_img_path(self) -> pathlib.Path:
        return self.img_path / "playlists"

    @property
    def assets_path(self) -> pathlib.Path:
        return self.config_dir / "assets"

    @property
    def plugins_path(self) -> pathlib.Path:
        return self.config_dir / "plugins"

    @property
    def lyrics_plugins_path(self) -> pathlib.Path:
        return self.plugins_path / "lyrics"

    @property
    def config_file_path(self) -> pathlib.Path:
        return self.config_dir / "settings.json"

    @property
    def mixes_img_path(self) -> pathlib.Path:
        return self.img_path / "mixes"

    @property
    def artist_mixes_img_path(self) -> pathlib.Path:
        return self.mixes_img_path / "artists"

    @property
    def og_mixes_img_path(self) -> pathlib.Path:
        return self.mixes_img_path / "original"

    @property
    def md_mixes_img_path(self) -> pathlib.Path:
        return self.mixes_img_path / "medium"

    @property
    def sm_mixes_img_path(self) -> pathlib.Path:
        return self.mixes_img_path / "small"

    @property
    def image_cache_path(self) -> pathlib.Path:
        return self.img_path / "cache"

    @property
    def app_db_path(self):
        return Paths().config_dir / self.APP_DB_NAME

    @property
    def userdata_db_path(self):
        return Paths().config_dir / self.USER_DATA_DB_NAME

    @property
    def json_config_path(self):
        return Paths().config_dir / "config.json"