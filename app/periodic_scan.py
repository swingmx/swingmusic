"""
This module contains functions for the server
"""
import time

from app.lib.populate import Populate, PopulateCancelledError
from app.settings import ParserFlags, get_flag, get_scan_sleep_time
from app.utils.generators import get_random_str
from app.utils.threading import background


@background
def run_periodic_scans():
    """
    Runs periodic scans.
    """
    # ValidateAlbumThumbs()
    # ValidatePlaylistThumbs()

    run_periodic_scan = True

    while run_periodic_scan:
        run_periodic_scan = get_flag(ParserFlags.DO_PERIODIC_SCANS)

        try:
            Populate(instance_key=get_random_str())
        except PopulateCancelledError:
            pass

        sleep_time = get_scan_sleep_time()
        time.sleep(sleep_time)
