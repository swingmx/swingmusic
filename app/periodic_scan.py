"""
This module contains functions for the server
"""
import time

from app.logger import log
from app.lib.populate import Populate, PopulateCancelledError

from app.utils.generators import get_random_str
from app.utils.network import Ping
from app.utils.threading import background

from app.settings import ParserFlags, get_flag, get_scan_sleep_time


@background
def run_periodic_scans():
    """
    Runs periodic scans.
    """
    # ValidateAlbumThumbs()
    # ValidatePlaylistThumbs()

    while get_flag(ParserFlags.DO_PERIODIC_SCANS):
        try:
            Populate(key=get_random_str())
        except PopulateCancelledError:
            pass

        sleep_time = get_scan_sleep_time()
        time.sleep(sleep_time)
