"""
Prepares the server for use.
"""
from app.setup.files import create_config_dir
from app.setup.sqlite import run_migrations, setup_sqlite
from app.store.albums import AlbumStore
from app.store.artists import ArtistStore
from app.store.tracks import TrackStore


def run_setup():
    create_config_dir()
    setup_sqlite()
    run_migrations()

    TrackStore.load_all_tracks()
    AlbumStore.load_albums()
    ArtistStore.load_artists()
