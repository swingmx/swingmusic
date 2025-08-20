"""
This file contains all global variables.
All Variables should be read only after an initial set.

Contains default configs
"""

import pathlib
import shutil
from pathlib import Path
import os
import logging

from swingmusic.utils.filesystem import get_home_res_path

log = logging.getLogger(__name__)

# # # # # # # # #
#  Meta-classes  #
# # # # # # # # #

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in Singleton._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# # # # # # # # #
#  Path  Logic  #
# # # # # # # # #


def default_base_path() -> pathlib.Path:
    """
    | Calculates the default config path for ``swingmusic``.
    | Checks for the first valid path.
    | If no Path is valid, will use Home dir (4.)

    Check order:

    1. Env:``SWINGMUSIC_XDG_CONFIG_DIR``
    2. Env:``xdg_config_home``
    3. <User Home>/.config
    4. <User Home>

    :return: Calculated Path
    """

    swing_xdg_config_home = os.environ.get("SWINGMUSIC_XDG_CONFIG_DIR")
    xdg_config_home = os.environ.get("xdg_config_home")
    alt_dir = pathlib.Path.home() / ".config"

    base_path = pathlib.Path.home()

    if not swing_xdg_config_home is None:
        base_path = pathlib.Path(swing_xdg_config_home)

    elif not xdg_config_home is None:
        base_path = pathlib.Path(xdg_config_home)

    elif alt_dir.exists():
        base_path = alt_dir

    return base_path


class Paths(metaclass=Singleton):
    """
    This class stores all paths for ``swingmusic``s config.
    * Configs
    * DBs
    * Assets
    * Cache

    This class is a singleton.
    You cannot change the config path later.

    Not multiprocessing save:
    Multiprocessing will create separate environment without configs
    """

    base_path:Path = Path.home().resolve()
    USER_HOME_DIR = Path.home().resolve()
    APP_DB_NAME = "swingmusic.db"
    USER_DATA_DB_NAME = "userdata.db"


    def __init__(self, base_path:Path=None):
        """
        Create config-folder structure and check permissions.
        Copy all assets if needed.

        :param self: Own object
        :param base_path: Parent path of ``swingmusic``s config path
        """

        """
        Returns the XDG_CONFIG_HOME environment variable if it exists, otherwise
        returns the default config directory. If none of those exist, returns the
        user's home directory.
        """

        if base_path is not None:
            self.base_path = base_path
        else:
            self.base_path = default_base_path()

        self.mkdir_config_folders()

        # set global easier access?
        global paths
        paths = self


    def mkdir_config_folders(self):
        """
        Create the config/cache folder structure.

        base folder
        └───`swingmusic` or `.swingmusic`
            ├───images
            │   ├───artists
            │   │   ├───large
            │   │   ├───medium
            │   │   └───small
            │   ├───mixes
            │   │   ├───medium
            │   │   ├───original
            │   │   └───small
            │   ├───playlists
            │   └───thumbnails
            │       ├───large
            │       ├───medium
            │       ├───small
            │       └───xsmall
            └───plugins
                └───lyrics
        """


        # all dirs relative to `swingmusic` config dir
        dirs = [
            "",                                 # `swingmusic` or `.swingmusic`
            "plugins/lyrics",
            "images/playlists",
            "images/thumbnails/small",
            "images/thumbnails/large",
            "images/thumbnails/medium",
            "images/thumbnails/xsmall",
            "images/artists/medium",
            "images/artists/small",
            "images/artists/large",
            "images/mixes/",
            "images/mixes/original",
            "images/mixes/medium",
            "images/mixes/small",
        ]

        for folder in dirs:
            path = self.base_path / self.config_folder_name / folder
            if not path.exists():
                path.mkdir(parents=True)
                path.chmod(mode=0o755)

        # Empty files to create
        empty_files = [
            # artist split ignore list
            self.app_dir / "data" / "artist_split_ignore.txt" # TODO: use USERCONFIG -> circular import error
        ]

        for file in empty_files:
            if file.is_dir():
                file.rmdir()

            if not file.exists():
                file.parent.mkdir(parents=True, exist_ok=True)
                file.touch()


    def copy_assets_dir(self):
        """
        Copies assets to the app directory.
        """

        # TODO: rework this function.
        #  Either import assets from inside the module, no need for copy
        #  or copy files with explicit location to config folder

        assets_dir = get_home_res_path("assets")

        src = assets_dir
        dest = (self.app_dir / "assets").resolve()

        if src.exists():
            shutil.copytree(
                src,
                dest,
                ignore=shutil.ignore_patterns(
                    "*.pyc",
                ),
                copy_function=shutil.copy2,
                dirs_exist_ok=True,
            )
        else:
            log.warning(f"Assets dir could not be found: {src.as_posix()}")


    @property
    def config_dir(self) -> pathlib.Path:
        """
        return the resolved base path of swingmusic config folder
        """
        return self.base_path.resolve()

    @property
    def config_folder_name(self) -> str:
        """
        return the name of the swingmusic config folder.

        When the base path is the same as the home dir,
        it returns `.swingmusic` else `swingmusic`
        """
        if self.config_dir == self.USER_HOME_DIR:
            return ".swingmusic"
        else:
            return "swingmusic"

    @property
    def app_dir(self) -> Path:
        return self.config_dir / self.config_folder_name

    @property
    def img_path(self) -> Path:
        return self.app_dir / "images"

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
        return self.thumbs_path/ "large"

    # OTHERS
    @property
    def playlist_img_path(self) -> pathlib.Path:
        return self.img_path / "playlists"

    @property
    def assets_path(self) -> pathlib.Path:
        return self.app_dir / "assets"

    @property
    def plugins_path(self) -> pathlib.Path:
        return self.app_dir / "plugins"

    @property
    def lyrics_plugins_path(self) -> pathlib.Path:
        return self.plugins_path / "lyrics"

    @property
    def config_file_path(self) -> pathlib.Path:
        return self.app_dir/ "settings.json"

    @property
    def mixes_img_path(self) -> pathlib.Path:
        return self.img_path/ "mixes"

    @property
    def artist_mixes_img_path(self) -> pathlib.Path:
        return self.mixes_img_path/ "artists"

    @property
    def og_mixes_img_path(self) -> pathlib.Path:
        return self.mixes_img_path/ "original"

    @property
    def md_mixes_img_path(self) -> pathlib.Path:
        return self.mixes_img_path/ "medium"

    @property
    def sm_mixes_img_path(self) -> pathlib.Path:
        return self.mixes_img_path / "small"

    @property
    def image_cache_path(self) -> pathlib.Path:
        return self.img_path / "cache"

    @property
    def app_db_path(self):
        return Paths().app_dir / self.APP_DB_NAME

    @property
    def userdata_db_path(self):
        return Paths().app_dir / self.USER_DATA_DB_NAME

    @property
    def json_config_path(self):
        return Paths().app_dir / "config.json"


# # # # # # # # # # # # #
# Default and Konstants #
# # # # # # # # # # # # #


class Defaults:
    """
    Contains default values for various settings.

    XSM_THUMB_SIZE: extra small thumbnail size for web client tracklist
    SM_THUMB_SIZE: small thumbnail size for android client tracklist
    MD_THUMB_SIZE: medium thumbnail size for web client album cards
    LG_THUMB_SIZE: large thumbnail size for web client now playing album art

    NOTE: LG_ARTIST_IMG_SIZE is undefined to save the images in their original size (500px)
    """

    XSM_THUMB_SIZE = 64
    SM_THUMB_SIZE = 96
    MD_THUMB_SIZE = 256
    LG_THUMB_SIZE = 512

    SM_ARTIST_IMG_SIZE = 128
    MD_ARTIST_IMG_SIZE = 256

    HASH_LENGTH = 16
    API_ALBUMHASH = "bfe300e966"
    API_ARTISTHASH = "cae59f1fc5"
    API_TRACKHASH = "0853280a12"
    API_ALBUMNAME = "The Goat"
    API_ARTISTNAME = "Polo G"
    API_TRACKNAME = "Martin & Gina"
    API_CARD_LIMIT = 6

class TCOLOR:
    """
    Terminal colors
    """

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    YELLOW = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    # credits: https://stackoverflow.com/a/287944