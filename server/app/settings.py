"""
Contains default configs
"""

import os

# paths
CONFIG_FOLDER = ".alice"
HOME_DIR = os.path.expanduser("~") + "/"
APP_DIR = os.path.join(HOME_DIR, CONFIG_FOLDER)
THUMBS_PATH = os.path.join(APP_DIR, "images", "thumbnails")

# URL
IMG_BASE_URI = "http://127.0.0.1:8900/images/"
IMG_ARTIST_URI = IMG_BASE_URI + "artists/"
IMG_THUMB_URI = IMG_BASE_URI + "thumbnails/"

# defaults
DEFAULT_ARTIST_IMG = IMG_ARTIST_URI + "0.webp"

LAST_FM_API_KEY = "762db7a44a9e6fb5585661f5f2bdf23a"
