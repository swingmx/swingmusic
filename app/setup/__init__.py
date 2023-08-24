"""
Prepares the server for use.
"""
from app.db.sqlite.settings import load_settings
from app.setup.files import create_config_dir
from app.setup.sqlite import run_migrations, setup_sqlite
from app.store.albums import AlbumStore
from app.store.artists import ArtistStore
from app.store.tracks import TrackStore
from app.utils.generators import get_random_str


def run_setup():
    create_config_dir()
    setup_sqlite()
    run_migrations()

    try:
        load_settings()
    except IndexError:
        # settings table is empty
        pass

    instance_key = get_random_str()

    TrackStore.load_all_tracks(instance_key)
    AlbumStore.load_albums(instance_key)
    ArtistStore.load_artists(instance_key)
