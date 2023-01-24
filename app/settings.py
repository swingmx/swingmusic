"""
Contains default configs
"""
import os


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
        alt_dir = os.path.join(os.environ.get("HOME"), ".config")

        if os.path.exists(alt_dir):
            return alt_dir
    except TypeError:
        return os.path.expanduser("~")


# ------- HELPER METHODS --------


APP_VERSION = "Swing v.1.0.0.beta.1"

# paths
XDG_CONFIG_DIR = get_xdg_config_dir()
USER_HOME_DIR = os.path.expanduser("~")

CONFIG_FOLDER = "swing" if XDG_CONFIG_DIR != USER_HOME_DIR else ".swing"

APP_DIR = os.path.join(XDG_CONFIG_DIR, CONFIG_FOLDER)
IMG_PATH = os.path.join(APP_DIR, "images")

ARTIST_IMG_PATH = os.path.join(IMG_PATH, "artists")
ARTIST_IMG_SM_PATH = os.path.join(ARTIST_IMG_PATH, "small")
ARTIST_IMG_LG_PATH = os.path.join(ARTIST_IMG_PATH, "large")

THUMBS_PATH = os.path.join(IMG_PATH, "thumbnails")
SM_THUMB_PATH = os.path.join(THUMBS_PATH, "small")
LG_THUMBS_PATH = os.path.join(THUMBS_PATH, "large")
MUSIC_DIR = os.path.join(USER_HOME_DIR, "Music")


# TEST_DIR = "/home/cwilvx/Downloads/Telegram Desktop"
# TEST_DIR = "/mnt/dfc48e0f-103b-426e-9bf9-f25d3743bc96/Music/Chill/Wolftyla Radio"
# HOME_DIR = TEST_DIR

# URLS
IMG_BASE_URI = "http://127.0.0.1:8900/images/"
IMG_ARTIST_URI = IMG_BASE_URI + "artists/"
IMG_THUMB_URI = IMG_BASE_URI + "thumbnails/"
IMG_PLAYLIST_URI = IMG_BASE_URI + "playlists/"

# defaults
DEFAULT_ARTIST_IMG = IMG_ARTIST_URI + "0.webp"

LAST_FM_API_KEY = "762db7a44a9e6fb5585661f5f2bdf23a"

THUMB_SIZE = 400
SM_THUMB_SIZE = 64
SM_ARTIST_IMG_SIZE = 64
"""
The size of extracted images in pixels
"""

FILES = ["flac", "mp3", "wav", "m4a"]
SUPPORTED_FILES = tuple(f".{file}" for file in FILES)

# ===== SQLite =====
APP_DB_NAME = "swing.db"
USER_DATA_DB_NAME = "userdata.db"
APP_DB_PATH = os.path.join(APP_DIR, APP_DB_NAME)
USERDATA_DB_PATH = os.path.join(APP_DIR, USER_DATA_DB_NAME)


# ===== Store =====
USE_STORE = True

HELP_MESSAGE = """
Usage: swingmusic [options]

Options:
    --build: Build the application
    --host: Set the host
    --port: Set the port
    --help, -h: Show this help message
    --version, -v: Show the version
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
