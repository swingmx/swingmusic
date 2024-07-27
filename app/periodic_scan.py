"""
This module contains functions for the server
"""

import time

from app.config import UserConfig
from app.lib.populate import PopulateCancelledError
from app.utils.generators import get_random_str
from app.utils.threading import background
from app.logger import log


# @background
# def run_periodic_scans():
#     """
#     Runs periodic scans.

#     Periodic scans are checks that run every few minutes
#     in the background to do stuff like:
#     - checking for new music
#     - delete deleted entries
#     - downloading artist images, and other data.
#     """
#     # ValidateAlbumThumbs()
#     # ValidatePlaylistThumbs()

#     while UserConfig().enablePeriodicScans:

#         try:
#         except PopulateCancelledError:
#             log.error("'run_periodic_scans': Periodic scan cancelled.")
#             pass

#         time.sleep(UserConfig().scanInterval)
