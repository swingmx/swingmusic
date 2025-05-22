"""
Prepares the server for use.
"""

from time import time
import uuid
from swingmusic.lib.mapstuff import (
    map_album_colors,
    map_artist_colors,
    map_favorites,
    map_scrobble_data,
)
from swingmusic.setup.files import create_config_dir
from swingmusic.setup.sqlite import run_migrations, setup_sqlite
from swingmusic.store.albums import AlbumStore
from swingmusic.store.artists import ArtistStore
from swingmusic.store.folder import FolderStore
from swingmusic.store.tracks import TrackStore
from swingmusic.utils.generators import get_random_str
from swingmusic.config import UserConfig


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
