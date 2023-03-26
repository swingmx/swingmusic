"""
Contains default configs
"""
import os

join = os.path.join


# ------- HELPER METHODS --------
def get_xdg_config_dir():
    """
    Returns the XDG_CONFIG_HOME environment variable if it exists, otherwise
    returns the default config directory. If none of those exist, returns the
    user's home directory.
    """
    xdg_config_home = os.environ.get("XDG_CONFIG_HOME")

    if xdg_config_home:
        return xdg_config_home

    try:
        alt_dir = join(os.environ.get("HOME"), ".config")

        if os.path.exists(alt_dir):
            return alt_dir
    except TypeError:
        return os.path.expanduser("~")


# !------- HELPER METHODS --------!

class Release:
    APP_VERSION = "v1.2.0"


class Paths:
    XDG_CONFIG_DIR = get_xdg_config_dir()
    USER_HOME_DIR = os.path.expanduser("~")

    CONFIG_FOLDER = "swingmusic" if XDG_CONFIG_DIR != USER_HOME_DIR else ".swingmusic"

    APP_DIR = join(XDG_CONFIG_DIR, CONFIG_FOLDER)
    IMG_PATH = join(APP_DIR, "images")

    ARTIST_IMG_PATH = join(IMG_PATH, "artists")
    ARTIST_IMG_SM_PATH = join(ARTIST_IMG_PATH, "small")
    ARTIST_IMG_LG_PATH = join(ARTIST_IMG_PATH, "large")

    PLAYLIST_IMG_PATH = join(IMG_PATH, "playlists")

    THUMBS_PATH = join(IMG_PATH, "thumbnails")
    SM_THUMB_PATH = join(THUMBS_PATH, "small")
    LG_THUMBS_PATH = join(THUMBS_PATH, "large")

    # TEST_DIR = "/home/cwilvx/Downloads/Telegram Desktop"
    # TEST_DIR = "/mnt/dfc48e0f-103b-426e-9bf9-f25d3743bc96/Music/Chill/Wolftyla Radio"
    # HOME_DIR = TEST_DIR


class Urls:
    IMG_BASE_URI = "http://127.0.0.1:8900/images/"
    IMG_ARTIST_URI = IMG_BASE_URI + "artists/"
    IMG_THUMB_URI = IMG_BASE_URI + "thumbnails/"
    IMG_PLAYLIST_URI = IMG_BASE_URI + "playlists/"


# defaults
class Defaults:
    DEFAULT_ARTIST_IMG = Urls.IMG_ARTIST_URI + "0.webp"
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
    APP_DB_PATH = join(Paths.APP_DIR, APP_DB_NAME)
    USERDATA_DB_PATH = join(Paths.APP_DIR, USER_DATA_DB_NAME)
    JSON_CONFIG_PATH = join(Paths.APP_DIR, "config.json")


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
