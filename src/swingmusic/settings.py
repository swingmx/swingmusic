"""
This file contains all global variables.
All Variables should be read only after an initial set.

Contains default configs
"""

import io
import multiprocessing
import pathlib
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path
import os
import logging
import requests
from importlib import metadata, resources as imres

from swingmusic.utils import classproperty


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


class AssetHandler:
    """
    Handles all assets configuration
    """

    RELEASES_URL = "https://api.github.com/repos/swingmx/swingmusic/releases"

    @staticmethod
    def copy_assets_dir():
        """
        Copies assets to the app directory.
        """

        assets_source = imres.files("swingmusic") / "assets"
        assets_path = Paths().assets_path
        # INFO: this only works for wheels and source
        # TODO: Handle this for pyinstaller builds

        if assets_path.exists():
            # no need to copy what's already copied?
            return

        if assets_source.exists():
            shutil.copytree(
                Path(assets_source),
                assets_path,
                ignore=shutil.ignore_patterns(
                    "*.pyc",
                ),
                copy_function=shutil.copy2,
                dirs_exist_ok=True,
            )
        else:
            log.error(f"Assets dir could not be found: {assets_source.as_posix()}")

    @staticmethod
    def extract_default_client(path: Path) -> bool:
        """
        Extracts the default client which is bundled with the wheel
        into the swingmusic client folder.
        """
        # INFO: Locate the client.zip file using imres, extract it to the swingmusic client folder
        client_zip_path = imres.files("swingmusic") / "client.zip"
        if not client_zip_path.exists():
            # INFO: if client path contains an index.html file, return true
            if (path / "index.html").exists():
                return True

            return False

        with zipfile.ZipFile(client_zip_path, "r") as zip_ref:
            zip_ref.extractall(path)

        return True

    @staticmethod
    def process_release(release: dict, path: Path):
        """
        Processes a release from the GitHub API.
        """

        # INFO: find the client.zip asset
        for asset in release["assets"]:
            if asset["name"] == "client.zip":
                # download and extract client
                clientzip = requests.get(asset["browser_download_url"])
                mem_file = io.BytesIO(clientzip.content)
                file = zipfile.ZipFile(mem_file)

                # create new dir for extraction
                with tempfile.TemporaryDirectory() as temp_folder:
                    file.extractall(temp_folder)

                    shutil.copytree(
                        Path(temp_folder) / "client",
                        path,
                        copy_function=shutil.copy2,
                        dirs_exist_ok=True,
                    )

                log.info("Client downloaded successfully.")
                return True

        return False

    @staticmethod
    def download_client_from_github():
        """
        Downloads the latest supported client from Github
        and places it in the swingmusic client folder.
        """
        log.error("Default client not found. Downloading from GitHub ...")
        path = Paths().client_path

        try:
            # INFO: downlaod the current version of the client from GitHub
            releases = requests.get(AssetHandler.RELEASES_URL).json()

            # INFO: find the release for the current version
            for release in releases:
                if release["tag_name"] == f"v{Metadata.version}":
                    if AssetHandler.process_release(release, path):
                        return True
                    pass

            # INFO: if no release is found, download the latest release
            log.error(
                f"No release found for the v{Metadata.version}. Downloading latest version ..."
            )
            return AssetHandler.process_release(releases[0], path)

        except (
            requests.exceptions.RequestException,
            KeyError,
            requests.exceptions.ConnectionError,
        ) as e:
            log.error(
                "Client could not be downloaded from releases. NETWORK ERROR",
                exc_info=e,
            )
            return False
        except zipfile.BadZipfile as e:
            log.error("Client could not be unpacked. ZIP ERROR", exc_info=e)
            return False

    @classmethod
    def setup_default_client(cls):
        """
        Runs on startup to ensure the default client is present.
        """

        extracted = True
        client_path = Paths().client_path

        if not client_path.exists() or not (client_path / "index.html").exists():
            extracted = cls.extract_default_client(Paths().config_dir)

        if not extracted:
            extracted = cls.download_client_from_github()

        if not (client_path / "index.html").exists():
            log.error("Web client not found. Exiting ...")
            sys.exit(1)


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

    def __init__(
        self,
        config_parent: Path | None = None,
        client_dir: Path | None = None,
    ):
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

        if config_parent is not None:
            self.config_parent = config_parent.resolve()
        else:
            self.config_parent = Paths.get_default_config_parent_dir()

        if multiprocessing.current_process().name == "MainProcess":
            # INFO: Setup client path
            env_client_dir = os.environ.get("SWINGMUSIC_CLIENT_DIR")
            if client_dir is not None:
                self.client_path = client_dir.resolve()
            elif env_client_dir is not None:
                self.client_path = Path(env_client_dir).resolve()
            else:
                self.client_path = self.config_dir / "client"

            # Path copy only on MainProcess
            if not self.config_dir.exists():
                self.config_dir.mkdir(parents=True)

            # TODO: find a platform independent way to access module globals like `Paths`
            # TODO: move this into multithreading management class
            os.environ["SWINGMUSIC_CONFIG_DIR"] = (
                self.config_parent.resolve().as_posix()
            )
            os.environ["SWINGMUSIC_CLIENT_DIR"] = self.client_path.resolve().as_posix()

            self.setup_config_dirs()

    @classmethod
    def get_default_config_parent_dir(cls) -> pathlib.Path:
        """
        Determines the default config path in the following order:

        1. Env:``SWINGMUSIC_CONFIG_DIR``
        2. Env:``xdg_config_home``
        3. <User Home>/.config
        4. <User Home>

        :return: First valid path
        """

        config_dir_from_env = os.environ.get("SWINGMUSIC_CONFIG_DIR")
        xdg_config_home = os.environ.get("XDG_CONFIG_HOME")

        if config_dir_from_env is not None:
            return pathlib.Path(config_dir_from_env)

        if xdg_config_home is not None:
            return pathlib.Path(xdg_config_home)

        fallback_dir = pathlib.Path.home() / ".config"
        if fallback_dir.exists():
            return fallback_dir

        return pathlib.Path.home()

    def setup_config_dirs(self):
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
            "",  # `swingmusic` or `.swingmusic`
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
            path = self.config_parent / self.config_folder_name / folder
            if not path.exists():
                path.mkdir(parents=True)
                path.chmod(mode=0o755)

        # Empty files to create
        empty_files = [
            # artist split ignore list
            self.config_dir
            / "data"
            / "artist_split_ignore.txt"  # TODO: use USERCONFIG -> circular import error
        ]

        for file in empty_files:
            if file.is_dir():
                file.rmdir()

            if not file.exists():
                file.parent.mkdir(parents=True, exist_ok=True)
                file.touch()

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


class Metadata:
    """
    Contains metadata for the application.
    """

    @classproperty
    def version(self) -> str:
        version = metadata.version("swingmusic")

        if version == "0.0.0":
            return open("version.txt", "r").read().strip()

        return version
