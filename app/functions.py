"""
This module contains functions for the server
"""
import time

from requests import ConnectionError as RequestConnectionError
from requests import ReadTimeout

from app import utils
from app.lib.artistlib import CheckArtistImages
from app.lib.colorlib import ProcessAlbumColors
from app.lib.colorlib import ProcessArtistColors
from app.lib.populate import Populate
from app.lib.populate import ProcessTrackThumbnails
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

        Populate()
        ProcessTrackThumbnails()
        ProcessAlbumColors()
        ProcessArtistColors()

        if utils.Ping()():
            try:
                CheckArtistImages()
            except (RequestConnectionError, ReadTimeout):
                log.error(
                    "Internet connection lost. Downloading artist images stopped."
                )

        time.sleep(300)
