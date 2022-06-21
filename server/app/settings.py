"""
Contains default configs
"""
import os
import multiprocessing


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

P_COLORS = [
    "rgb(4, 40, 196)",
    "rgb(196, 4, 68)",
    "rgb(4, 99, 59)",
    "rgb(161, 87, 1)",
    "rgb(1, 161, 22)",
    "rgb(116, 1, 161)",
    "rgb(0, 0, 0)",
    "rgb(95, 95, 95)",
    "rgb(141, 132, 2)",
    "rgb(141, 11, 2)",
]

CPU_COUNT = multiprocessing.cpu_count()


class logger:
    enable = True
