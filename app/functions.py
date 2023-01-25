"""
This module contains functions for the server
"""
import time
from requests import ConnectionError as RequestConnectionError
from requests import ReadTimeout

from app import utils
from app.lib.artistlib import CheckArtistImages
from app.lib.colorlib import ProcessAlbumColors, ProcessArtistColors
from app.lib.populate import Populate, ProcessTrackThumbnails, PopulateCancelledError
from app.lib.trackslib import validate_tracks
from app.logger import log


@utils.background
def run_periodic_checks():
    """
    Checks for new songs every N minutes.
    """
    # ValidateAlbumThumbs()
    # ValidatePlaylistThumbs()
    validate_tracks()

    while True:
        try:
            Populate(key=utils.get_random_str())
        except PopulateCancelledError:
            pass

        if utils.Ping()():
            try:
                CheckArtistImages()
            except (RequestConnectionError, ReadTimeout):
                log.error(
                    "Internet connection lost. Downloading artist images stopped."
                )

        ProcessArtistColors()

        time.sleep(300)
