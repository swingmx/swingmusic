"""
This module contains functions for the server
"""
import time
from requests import ConnectionError as RequestConnectionError
from requests import ReadTimeout

from app.lib.artistlib import CheckArtistImages
from app.lib.populate import Populate, PopulateCancelledError
from app.lib.trackslib import validate_tracks
from app.logger import log
from app.utils.generators import get_random_str
from app.utils.network import Ping
from app.utils.threading import background


@background
def run_periodic_checks():
    """
    Checks for new songs every N minutes.
    """
    # ValidateAlbumThumbs()
    # ValidatePlaylistThumbs()
    validate_tracks()

    while True:
        try:
            Populate(key=get_random_str())
        except PopulateCancelledError:
            pass

        if Ping()():
            try:
                CheckArtistImages()
            except (RequestConnectionError, ReadTimeout):
                log.error(
                    "Internet connection lost. Downloading artist images stopped."
                )

        time.sleep(300)
