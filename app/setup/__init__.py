"""
Prepares the server for use.
"""
from app.db.store import Store
from app.setup.files import create_config_dir
from app.setup.sqlite import setup_sqlite, run_migrations


def run_setup():
    create_config_dir()
    setup_sqlite()
    run_migrations()

    Store.load_all_tracks()
    Store.process_folders()
    Store.load_albums()
    Store.load_artists()
