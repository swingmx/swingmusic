"""
Prepares the server for use.
"""

from time import time
import uuid
from app.lib.mapstuff import (
    map_album_colors,
    map_artist_colors,
    map_favorites,
    map_scrobble_data,
)
from app.setup.files import create_config_dir
from app.setup.sqlite import run_migrations, setup_sqlite
from app.store.albums import AlbumStore
from app.store.artists import ArtistStore
from app.store.folder import FolderStore
from app.store.tracks import TrackStore
from app.utils.generators import get_random_str
from app.config import UserConfig


def run_setup():
    """
    Creates the config directory, runs migrations, and loads settings.
    """
    create_config_dir()

    # setup config file
    config = UserConfig()
    config.setup_config_file()

    if not config.serverId:
        config.serverId = str(uuid.uuid4())

    setup_sqlite()
    run_migrations()


def load_into_mem():
    """
    Load all tracks, albums, and artists into memory.
    """
    # INFO: Load all tracks, albums, and artists data into memory
    key = str(time())
    TrackStore.load_all_tracks(get_random_str())
    AlbumStore.load_albums(key)
    ArtistStore.load_artists(key)
    FolderStore.load_filepaths()

    map_scrobble_data()
    map_favorites()
    map_artist_colors()
    map_album_colors()
