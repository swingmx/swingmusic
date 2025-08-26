"""
This file contains all global variables.
All Variables should be read only after an initial set.

Contains default configs
"""
import io
import multiprocessing
import pathlib
import shutil
import tempfile
import zipfile
from pathlib import Path
import os
import logging
import requests
from importlib import resources as imres


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

# # # # # # # #
# Downloader  #
# # # # # # # #

def populate_client(path:Path) -> bool:
        """
        Checks if client folder contains content.
        Client needs to have at least an index.html file.
        If not, latest client is parsed from GitHub builds.

        :param path: path to client folder
        :return: True if successful else False
        """

        CLIENT_RELEASES_URL = "https://api.github.com/repos/michilyy/swingmusic/releases/latest"
        # TODO: update to real client repo

        # TODO: check for new releases. Currently only download when client is not found
        # TODO: move this outside. `Paths` only does path routing.

        index = path / "index.html"
        if not index.exists():
            log.warning(f"'index.html' could not be found in '{path.as_posix()}'.")
            log.warning("Try downloading latest client from GitHub.")
            try:

                answer = requests.get(CLIENT_RELEASES_URL).json()

                for asset in answer["assets"]:
                    if asset["name"] == "client.zip":
                        # download and convert client
                        client = requests.get(asset["browser_download_url"])
                        mem_file = io.BytesIO(client.content)
                        file = zipfile.ZipFile(mem_file)

                        # create new dir for extraction
                        log.info(f"Storing client in '{path.as_posix()}'.")
                        with tempfile.TemporaryDirectory() as temp_folder:
                            file.extractall(temp_folder)

                            shutil.copytree(
                                Path(temp_folder) / "client",
                                path,
                                copy_function=shutil.copy2,
                                dirs_exist_ok=True,
                            )

                        break

            except (requests.exceptions.RequestException, KeyError, requests.exceptions.ConnectionError)as e:
                log.error(f"Client could not be downloaded from releases. NETWORK ERROR", exc_info=e)
                return False
            except requests.exceptions.InvalidJSONError as e:
                log.error(f"Client could not be downloaded from releases. JSON ERROR", exc_info=e)
                return False
            except zipfile.BadZipfile as e:
                log.error(f"Client could not be unpacked. ZIP ERROR", exc_info=e)
                return False

        return True

# # # # # # # # #
#  Path  Logic  #
# # # # # # # # #

def default_client_path(app_dir:Path, fallback_client:Path|None=None) -> Path:
    """
    | Calculates the default config path for ``client``.
    | Checks for the first valid path.

    Check order:

    1. Env:``SWINGMUSIC_CLIENT_DIR``
    2. if ``<app_dir>/client/`` exists
        1. use ``<app_dir>/client/``
    3. if ``<app_dir>/client/`` not exists
        1. try downloading client from GitHub
        2. if successful
            1. use ``<app_dir>/client/``
        3. if not successful
            1. use ``<fallback_client>``

    :param app_dir:
    :param fallback_client: optional path to client. Used in pyinstaller/AppImage build
    :return: Calculated Path
    """

    client_path = app_dir / 'client'

    env_client_dir = os.environ.get("SWINGMUSIC_CLIENT_DIR")

    if not env_client_dir is None:
        return Path(env_client_dir)


    if (client_path / "index.html").exists():
        return client_path
    else:
        if populate_client(client_path):
            return client_path
        elif fallback_client is not None:
            return fallback_client
        else:
            raise NotImplementedError(f"Client could not be determined. Neither download or fallback.")


def default_base_path() -> pathlib.Path:
    """
    | Calculates the default config path for ``swingmusic``.
    | Checks for the first valid path.
    | If no Path is valid, will use Home dir (4.)

    Check order:

    1. Env:``SWINGMUSIC_CONFIG_DIR``
    2. Env:``xdg_config_home``
    3. <User Home>/.config
    4. <User Home>

    :return: Calculated Path
    """

    swing_xdg_config_home = os.environ.get("SWINGMUSIC_CONFIG_DIR")
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
    """

    base_path:Path = Path.home().resolve()
    USER_HOME_DIR = Path.home().resolve()
    APP_DB_NAME = "swingmusic.db"
    USER_DATA_DB_NAME = "userdata.db"


    def __init__(self, config:Path|None=None, client:Path|None=None, fallback:Path|None=None):
        """
        Create config-folder structure and check permissions.
        Copy all assets if needed.

        If `config` or `client` are provided, they are used exclusively.
        In case of multithread, the environment vars are used.
        The detailed decision can be viewed in :func:`default_base_path`.

        :param self: Own object
        :param config: Parent path of ``swingmusic``s config path.
        :param client: Path to static Web client folder.c
        :param fallback: Path to fallback client folder.
        """

        """
        Returns the XDG_CONFIG_HOME environment variable if it exists, otherwise
        returns the default config directory. If none of those exist, returns the
        user's home directory.
        """

        if config is not None:
            self.base_path = config.resolve()
        else:
            self.base_path = default_base_path()

        env_client_dir = os.environ.get("SWINGMUSIC_CLIENT_DIR")
        if client is not None:
            self.client_path = client.resolve()
        elif not env_client_dir is None:
            self.client_path = Path(env_client_dir)
        else:
            self.client_path = default_client_path(self.app_dir, fallback)

        if multiprocessing.current_process().name == "MainProcess":
            # Path copy only on MainProcess
            if not self.app_dir.exists():
                self.app_dir.mkdir(parents=True)

            # TODO: find a platform independent way to access module globals like `Paths`
            # TODO: move this into multithreading management class
            os.environ["SWINGMUSIC_CONFIG_DIR"] = self.base_path.resolve().as_posix()
            os.environ["SWINGMUSIC_CLIENT_DIR"] = self.client_path.resolve().as_posix()

            self.mkdir_config_folders()
            self.copy_assets_dir()


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

        assets_source = imres.files("swingmusic") / "assets"

        if self.assets_path.exists():
            # no need to copy what's already copied
            return

        if assets_source.exists():
            shutil.copytree(
                Path(assets_source),
                self.assets_path,
                ignore=shutil.ignore_patterns(
                    "*.pyc",
                ),
                copy_function=shutil.copy2,
                dirs_exist_ok=True,
            )
        else:
            log.error(f"Assets dir could not be found: {assets_source.as_posix()}")


    @property
    def config_folder_name(self) -> str:
        """
        return the name of the swingmusic config folder.

        When the base path is the same as the home dir,
        it returns `.swingmusic` else `swingmusic`
        """
        if self.base_path == self.USER_HOME_DIR:
            return ".swingmusic"
        else:
            return "swingmusic"

    @property
    def app_dir(self) -> Path:
        return self.base_path / self.config_folder_name

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