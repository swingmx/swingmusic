"""
This module contains all the Flask Blueprints and API routes. It also contains all the globals list
that are used through-out the app. It handles the initialization of the watchdog,
checking and creating config dirs and starting the re-indexing process using a background thread.
"""
from typing import List
from typing import Set

from app import functions
from app import helpers
from app import instances
from app import models
from app import prep
from app.lib import albumslib
from app.lib import folderslib
from app.lib import playlistlib

DB_TRACKS = instances.tracks_instance.get_all_tracks()
VALID_FOLDERS: Set[str] = set()

ALBUMS: List[models.Album] = []
TRACKS: List[models.Track] = []
PLAYLISTS: List[models.Playlist] = []
FOLDERS: List[models.Folder] = List


@helpers.background
def initialize() -> None:
    """
    Runs all the necessary setup functions.
    """
    functions.start_watchdog()
    prep.create_config_dir()
    albumslib.create_everything()
    folderslib.run_scandir()
    playlistlib.create_all_playlists()
    # functions.reindex_tracks()


initialize()
