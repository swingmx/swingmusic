"""
Contains the functions to prepare the server for use.
"""
import os
import shutil
from configparser import ConfigParser

from app import settings
from app.db.sqlite import create_connection, create_tables, queries
from app.db.store import Store
from app.settings import APP_DB_PATH, USERDATA_DB_PATH
from app.utils import get_home_res_path

config = ConfigParser()

config_path = get_home_res_path("pyinstaller.config.ini")
config.read(config_path)


try:
    IS_BUILD = config["DEFAULT"]["BUILD"] == "True"
except KeyError:
    # If the key doesn't exist, it means that the app is being executed in dev mode.
    IS_BUILD = False


class CopyFiles:
    """Copies assets to the app directory."""

    def __init__(self) -> None:
        assets_dir = "assets"

        if IS_BUILD:
            assets_dir = get_home_res_path("assets")

        files = [
            {
                "src": assets_dir,
                "dest": os.path.join(settings.APP_DIR, "assets"),
                "is_dir": True,
            }
        ]

        for entry in files:
            src = os.path.join(os.getcwd(), entry["src"])

            if entry["is_dir"]:
                shutil.copytree(
                    src,
                    entry["dest"],
                    ignore=shutil.ignore_patterns(
                        "*.pyc",
                    ),
                    copy_function=shutil.copy2,
                    dirs_exist_ok=True,
                )
                break

            shutil.copy2(src, entry["dest"])


def create_config_dir() -> None:
    """
    Creates the config directory if it doesn't exist.
    """

    home_dir = os.path.expanduser("~")
    config_folder = os.path.join(home_dir, settings.CONFIG_FOLDER)

    thumb_path = os.path.join("images", "thumbnails")
    small_thumb_path = os.path.join(thumb_path, "small")
    large_thumb_path = os.path.join(thumb_path, "large")

    artist_img_path = os.path.join("images", "artists")
    small_artist_img_path = os.path.join(artist_img_path, "small")
    large_artist_img_path = os.path.join(artist_img_path, "large")

    playlist_img_path = os.path.join("images", "playlists")

    dirs = [
        "",  # creates the config folder
        "images",
        thumb_path,
        small_thumb_path,
        large_thumb_path,
        artist_img_path,
        small_artist_img_path,
        large_artist_img_path,
        playlist_img_path,
    ]

    for _dir in dirs:
        path = os.path.join(config_folder, _dir)
        exists = os.path.exists(path)

        if not exists:
            os.makedirs(path)
            os.chmod(path, 0o755)

    CopyFiles()


def setup_sqlite():
    """
    Create Sqlite databases and tables.
    """
    # if os.path.exists(DB_PATH):
    #     os.remove(DB_PATH)

    app_db_conn = create_connection(APP_DB_PATH)
    playlist_db_conn = create_connection(USERDATA_DB_PATH)

    create_tables(app_db_conn, queries.CREATE_APPDB_TABLES)
    create_tables(playlist_db_conn, queries.CREATE_USERDATA_TABLES)

    app_db_conn.close()
    playlist_db_conn.close()

    Store.load_all_tracks()
    Store.process_folders()
    Store.load_albums()
    Store.load_artists()


def run_setup():
    create_config_dir()
    setup_sqlite()
