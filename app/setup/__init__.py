"""
Prepares the server for use.
"""

import uuid
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

    # try:
    #     load_settings()
    # except IndexError:
    #     # settings table is empty
    #     pass


def load_into_mem():
    """
    Load all tracks, albums, and artists into memory.
    """
    # instance_key = get_random_str()

    # INFO: Load all tracks, albums, and artists into memory
    # TrackStore.load_all_tracks(instance_key)
    # AlbumStore.load_albums(instance_key)
    # ArtistStore.load_artists(instance_key)
    TrackStore.load_all_tracks(get_random_str())
    FolderStore.load_filepaths()