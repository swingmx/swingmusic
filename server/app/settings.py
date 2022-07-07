"""
Contains default configs
"""
import multiprocessing
import os

# paths
CONFIG_FOLDER = ".alice"
HOME_DIR = os.path.expanduser("~")
APP_DIR = os.path.join(HOME_DIR, CONFIG_FOLDER)
IMG_PATH = os.path.join(APP_DIR, "images")

THUMBS_PATH = os.path.join(IMG_PATH, "thumbnails")
TEST_DIR = "/home/cwilvx/Music/Link to Music/Chill/Wolftyla Radio"
# HOME_DIR = TEST_DIR

# URLS
IMG_BASE_URI = "http://127.0.0.1:8900/images/"
IMG_ARTIST_URI = IMG_BASE_URI + "artists/"
IMG_THUMB_URI = IMG_BASE_URI + "thumbnails/"
IMG_PLAYLIST_URI = IMG_BASE_URI + "playlists/"

# defaults
DEFAULT_ARTIST_IMG = IMG_ARTIST_URI + "0.webp"

LAST_FM_API_KEY = "762db7a44a9e6fb5585661f5f2bdf23a"

CPU_COUNT = multiprocessing.cpu_count()

THUMB_SIZE: int = 400
"""
The size of extracted in pixels
"""

LOGGER_ENABLE: bool = True
