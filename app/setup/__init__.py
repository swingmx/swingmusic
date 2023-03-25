"""
Prepares the server for use.
"""
from app.store.store import FolderStore
from app.setup.files import create_config_dir
from app.setup.sqlite import setup_sqlite, run_migrations

from app.store.albums import AlbumStore
from app.store.tracks import TrackStore
from app.store.artists import ArtistStore


def run_setup():
    create_config_dir()
    setup_sqlite()
    run_migrations()

    TrackStore.load_all_tracks()
    FolderStore.process_folders()
    AlbumStore.load_albums()
    ArtistStore.load_artists()
