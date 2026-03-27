import time
import schedule

from swingmusic.crons.license import LicenseValidation
from swingmusic.crons.mixes import Mixes
from swingmusic.lib.recipes.recents import RecentlyAdded, RecentlyPlayed
from swingmusic.lib.recipes.topstreamed import TopArtists
from swingmusic.utils.threading import background


@background
def start_cron_jobs(and_exit: bool = False):
    """
    This is the function that triggers the cron jobs.
    """
    # NOTE: RecentlyPlayed is not a CRON job, it's triggered here to
    # populate the values for the very first time.
    print("start_cron_jobs")
    RecentlyPlayed()
    RecentlyAdded()

    # Initialized CRON jobs
    TopArtists()
    TopArtists(duration="week")
    Mixes()
    LicenseValidation()

    # Trigger all CRON jobs when the app is started.
    schedule.run_all()

    # To manually trigger cron jobs, only once
    if and_exit:
        return

    # Run all CRON jobs on a loop.
    while True:
        schedule.run_pending()
        time.sleep(1)
