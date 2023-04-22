"""
Contains default configs
"""
import os

join = os.path.join


class Release:
    APP_VERSION = "v1.2.1"


class Paths:
    XDG_CONFIG_DIR = ""
    USER_HOME_DIR = os.path.expanduser("~")

    # TODO: Break this down into getter methods for each path

    @classmethod
    def set_config_dir(cls, path: str):
        cls.XDG_CONFIG_DIR = path

    @classmethod
    def get_config_dir(cls):
        return cls.XDG_CONFIG_DIR

    @classmethod
    def get_config_folder(cls):
        return "swingmusic" if cls.get_config_dir() != cls.USER_HOME_DIR else ".swingmusic"

    @classmethod
    def get_app_dir(cls):
        return join(cls.get_config_dir(), cls.get_config_folder())

    @classmethod
    def get_img_path(cls):
        return join(cls.get_app_dir(), "images")

    @classmethod
    def get_artist_img_path(cls):
        return join(cls.get_img_path(), "artists")

    @classmethod
    def get_artist_img_sm_path(cls):
        return join(cls.get_artist_img_path(), "small")

    @classmethod
    def get_artist_img_lg_path(cls):
        return join(cls.get_artist_img_path(), "large")

    @classmethod
    def get_playlist_img_path(cls):
        return join(cls.get_img_path(), "playlists")

    @classmethod
    def get_thumbs_path(cls):
        return join(cls.get_img_path(), "thumbnails")

    @classmethod
    def get_sm_thumb_path(cls):
        return join(cls.get_thumbs_path(), "small")

    @classmethod
    def get_lg_thumb_path(cls):
        return join(cls.get_thumbs_path(), "large")

    @classmethod
    def get_assets_path(cls):
        return join(Paths.get_app_dir(), "assets")


# defaults
class Defaults:
    THUMB_SIZE = 400
    SM_THUMB_SIZE = 64
    SM_ARTIST_IMG_SIZE = 64
    """
    The size of extracted images in pixels
    """


FILES = ["flac", "mp3", "wav", "m4a", "ogg", "wma", "opus", "alac", "aiff"]
SUPPORTED_FILES = tuple(f".{file}" for file in FILES)


# ===== SQLite =====
class Db:
    APP_DB_NAME = "swing.db"
    USER_DATA_DB_NAME = "userdata.db"

    @classmethod
    def get_app_db_path(cls):
        return join(Paths.get_app_dir(), cls.APP_DB_NAME)

    @classmethod
    def get_userdata_db_path(cls):
        return join(Paths.get_app_dir(), cls.USER_DATA_DB_NAME)

    @classmethod
    def get_json_config_path(cls):
        return join(Paths.get_app_dir(), "config.json")


class FLASKVARS:
    FLASK_PORT = 1970
    FLASK_HOST = "localhost"


class ALLARGS:
    """
    Enumerates the possible app arguments.
    """

    build = "--build"
    port = "--port"
    host = "--host"
    config = "--config"
    show_feat = ["--show-feat", "-sf"]
    show_prod = ["--show-prod", "-sp"]
    help = ["--help", "-h"]
    version = ["--version", "-v"]


class FromFlags:
    EXTRACT_FEAT = True
    """
    Whether to extract the featured artists from the song title.
    """

    REMOVE_PROD = True
    """
    Whether to remove the producers from the song title.
    """

    REMOVE_REMASTER = True
    MERGE_REMASTERS = True


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


class Keys:
    # get last fm api key from os environment
    LASTFM_API = os.environ.get("LASTFM_API_KEY")
