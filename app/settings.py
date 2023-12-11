"""
Contains default configs
"""
import os
import sys
from typing import Any

from app import configs

join = os.path.join

if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    IS_BUILD = True
else:
    IS_BUILD = False


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
        return (
            "swingmusic" if cls.get_config_dir() != cls.USER_HOME_DIR else ".swingmusic"
        )

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
    def get_original_thumb_path(cls):
        return join(cls.get_thumbs_path(), "original")

    @classmethod
    def get_assets_path(cls):
        return join(Paths.get_app_dir(), "assets")

    @classmethod
    def get_plugins_path(cls):
        return join(Paths.get_app_dir(), "plugins")

    @classmethod
    def get_lyrics_plugins_path(cls):
        return join(Paths.get_plugins_path(), "lyrics")


# defaults
class Defaults:
    THUMB_SIZE = 500
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


# TODO: Find a way to eliminate this class without breaking typings
class SessionVarKeys:
    EXTRACT_FEAT = "EXTRACT_FEAT"
    REMOVE_PROD = "REMOVE_PROD"
    CLEAN_ALBUM_TITLE = "CLEAN_ALBUM_TITLE"
    REMOVE_REMASTER_FROM_TRACK = "REMOVE_REMASTER_FROM_TRACK"
    DO_PERIODIC_SCANS = "DO_PERIODIC_SCANS"
    PERIODIC_SCAN_INTERVAL = "PERIODIC_SCAN_INTERVAL"
    MERGE_ALBUM_VERSIONS = "MERGE_ALBUM_VERSIONS"
    ARTIST_SEPARATORS = "ARTIST_SEPARATORS"
    SHOW_ALBUMS_AS_SINGLES = "SHOW_ALBUMS_AS_SINGLES"


def get_flag(key: SessionVarKeys) -> bool:
    return getattr(SessionVars, key)


def set_flag(key: SessionVarKeys, value: Any):
    setattr(SessionVars, key, value)


def get_scan_sleep_time() -> int:
    return SessionVars.PERIODIC_SCAN_INTERVAL


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
    LASTFM_API_KEY = os.environ.get("LASTFM_API_KEY")
    PLUGIN_LYRICS_AUTHORITY = os.environ.get("PLUGIN_LYRICS_AUTHORITY")
    PLUGIN_LYRICS_ROOT_URL = os.environ.get("PLUGIN_LYRICS_ROOT_URL")
    SWINGMUSIC_APP_VERSION = os.environ.get("SWINGMUSIC_APP_VERSION")

    @classmethod
    def load(cls):
        if IS_BUILD:
            cls.LASTFM_API_KEY = configs.LASTFM_API_KEY
            cls.PLUGIN_LYRICS_AUTHORITY = configs.PLUGIN_LYRICS_AUTHORITY
            cls.PLUGIN_LYRICS_ROOT_URL = configs.PLUGIN_LYRICS_ROOT_URL
            cls.SWINGMUSIC_APP_VERSION = configs.SWINGMUSIC_APP_VERSION

        cls.verify_keys()

    @classmethod
    def verify_keys(cls):
        if not cls.LASTFM_API_KEY:
            print("ERROR: LASTFM_API_KEY not set in environment")
            sys.exit(0)

    @classmethod
    def get(cls, key: str):
        return getattr(cls, key, None)
