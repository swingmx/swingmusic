"""
Contains default configs
"""
import pathlib
from pathlib import Path
import os
import subprocess
import sys

from swingmusic import configs
from swingmusic.utils.filesystem import get_home_res_path


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]



if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    IS_BUILD = True
else:
    IS_BUILD = False


class Paths(metaclass=SingletonMeta):
    """
    This class is a singleton.
    That means only the first instantiation of Paths can set the swingmusic config path.
    You cannot change the config path later.
    """

    base_path:Path = Path.home().resolve()
    USER_HOME_DIR = Path.home().resolve()


    def __init__(self, base_path:Path=None):
        """
        Create config-folder structure and check permissions.
        This Class can be used

        :param base_path: The location where the swingmusic config folder will be created.
        """

        """
        Returns the XDG_CONFIG_HOME environment variable if it exists, otherwise
        returns the default config directory. If none of those exist, returns the
        user's home directory.
        """

        xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
        swing_xdg_config_home = os.environ.get("SWINGMUSIC_XDG_CONFIG_DIR")
        alt_dir = Path.home() / ".config"


        if not base_path is None:
            self.base_path = Path(base_path)

        elif not swing_xdg_config_home is None:
            self.base_path = Path(swing_xdg_config_home)

        elif not xdg_config_home is None:
            self.base_path =  Path(xdg_config_home)

        elif alt_dir.exists():
            self.base_path = alt_dir

        else:
            self.base_path = Path.home()

        self.mkdir_config_folders()


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
    def md_artist_img_path(self):
        return self.artist_img_path / "medium"

    @property
    def lg_artist_img_path(self):
        return self.artist_img_path / "large"

    # TRACK THUMBNAILS
    @property
    def thumbs_path(self):
        return self.img_path / "thumbnails"

    @property
    def sm_thumb_path(self):
        return self.thumbs_path / "small"

    @property
    def xsm_thumb_path(self):
        return self.thumbs_path / "xsmall"

    @property
    def md_thumb_path(self):
        return self.thumbs_path / "medium"

    @property
    def lg_thumb_path(self):
        return self.thumbs_path/ "large"

    # OTHERS
    @property
    def playlist_img_path(self):
        return self.img_path / "playlists"

    def assets_path(self):
        return self.app_dir / "assets"

    @property
    def plugins_path(self):
        return self.app_dir / "plugins"

    @property
    def lyrics_plugins_path(self):
        return self.plugins_path / "lyrics"

    @property
    def config_file_path(self):
        return self.app_dir/ "settings.json"

    @property
    def mixes_img_path(self):
        return self.img_path/ "mixes"

    @property
    def artist_mixes_img_path(self):
        return self.mixes_img_path/ "artists"

    @property
    def og_mixes_img_path(self):
        return self.mixes_img_path/ "original"

    @property
    def md_mixes_img_path(self):
        return self.mixes_img_path/ "medium"

    @property
    def sm_mixes_img_path(self):
        return self.mixes_img_path / "small"

    @property
    def image_cache_path(self):
        return self.img_path / "cache"


# defaults
class Defaults:
    """
    Contains default values for various settings.

    XSM_THUMB_SIZE: extra small thumbnail size for web client tracklist
    SM_THUMB_SIZE: small thumbnail size for android client tracklist
    MD_THUMB_SIZE: medium thumbnail size for web client album cards
    LG_THUMB_SIZE: large thumbnail size for web client now playing album art

    NOTE: LG_ARTIST_IMG_SIZE is not defined as the images are saved in the original size (500px)
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


# ===== SQLite =====
class DbPaths:
    APP_DB_NAME = "swingmusic.db"
    USER_DATA_DB_NAME = "userdata.db"

    @classmethod
    def get_app_db_path(cls):
        return Paths().app_dir / cls.APP_DB_NAME

    @classmethod
    def get_userdata_db_path(cls):
        return Paths().app_dir / cls.USER_DATA_DB_NAME

    @classmethod
    def get_json_config_path(cls):
        return Paths().app_dir / "config.json"


class FLASKVARS:
    FLASK_PORT = 1970
    FLASK_HOST = "localhost"

    @classmethod
    def get_flask_port(cls):
        return cls.FLASK_PORT

    @classmethod
    def get_flask_host(cls):
        return cls.FLASK_HOST

    @classmethod
    def set_flask_port(cls, port):
        cls.FLASK_PORT = port

    @classmethod
    def set_flask_host(cls, host):
        cls.FLASK_HOST = host


class ALLARGS:
    """
    Enumerates the possible app arguments.
    """

    build = "--build"
    port = "--port"
    host = "--host"
    config = "--config"

    pswd = "--pswd"

    show_feat = ("--show-feat", "-sf")
    show_prod = ("--show-prod", "-sp")
    dont_clean_albums = ("--no-clean-albums", "-nca")
    dont_clean_tracks = ("--no-clean-tracks", "-nct")
    no_periodic_scan = ("--no-periodic-scan", "-nps")
    periodic_scan_interval = ("--scan-interval", "-psi")

    help = ("--help", "-h")
    version = ("--version", "-v")


class SessionVars:
    """
    Variables that can be altered per session.
    """

    EXTRACT_FEAT = True
    """
    Whether to extract the featured artists from the song title.
    """

    REMOVE_PROD = True
    """
    Whether to remove the producers from the song title.
    """

    CLEAN_ALBUM_TITLE = True
    REMOVE_REMASTER_FROM_TRACK = True

    DO_PERIODIC_SCANS = True
    PERIODIC_SCAN_INTERVAL = 600  # 10 minutes
    """
    The interval between periodic scans in seconds.
    """

    MERGE_ALBUM_VERSIONS = False
    ARTIST_SEPARATORS = set()
    SHOW_ALBUMS_AS_SINGLES = False


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


def getLatestCommitHash():
    """
    Returns the latest git commit hash for the current branch
    """

    try:
        hash = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
        return hash.decode("utf-8").strip()
    except:
        return ""


def getCurrentBranch():
    """
    Returns the current git branch
    """

    try:
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"])
        return branch.decode("utf-8").strip()
    except:
        return ""


class Info:
    """
    Contains information about the app

    NOTE: This class initially written to load keys when running in build mode.
    TODO: Remove this class entirely, and implement functionality where needed.
    """

    SWINGMUSIC_APP_VERSION = os.environ.get("SWINGMUSIC_APP_VERSION")

    if not SWINGMUSIC_APP_VERSION:
        path = get_home_res_path("version.txt")
        if not path:
            raise ValueError("Version file not found")

        with open(path, "r") as f:
            SWINGMUSIC_APP_VERSION = f.read().strip()

    GIT_LATEST_COMMIT_HASH = "<unset>"
    GIT_CURRENT_BRANCH = "<unset>"

    @classmethod
    def load(cls):
        if IS_BUILD:
            cls.SWINGMUSIC_APP_VERSION = configs.SWINGMUSIC_APP_VERSION
            cls.GIT_LATEST_COMMIT_HASH = configs.GIT_LATEST_COMMIT_HASH
            cls.GIT_CURRENT_BRANCH = configs.GIT_CURRENT_BRANCH
        else:
            cls.GIT_LATEST_COMMIT_HASH = getLatestCommitHash()
            cls.GIT_CURRENT_BRANCH = getCurrentBranch()

    @classmethod
    def get(cls, key: str):
        return getattr(cls, key, None)
