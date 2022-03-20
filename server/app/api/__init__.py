from typing import List

from app import models, instances
from app import functions, helpers, albumslib, prep


DB_TRACKS = instances.songs_instance.get_all_songs()
ALBUMS: List[models.Album] = []
TRACKS: List[models.Track] = []


@helpers.background
def initialize() -> None:
    """
    Runs all the necessary setup functions.
    """
    functions.start_watchdog()
    albumslib.create_everything()
    prep.create_config_dir()
    functions.reindex_tracks()


initialize()
