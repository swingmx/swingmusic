import time
import schedule

from app.crons.mixes import Mixes
from app.lib.recipes.recents import RecentlyAdded, RecentlyPlayed
from app.lib.recipes.topstreamed import TopArtists
from app.utils.threading import background


@background
def start_cron_jobs():
    """
    This is the function that triggers the cron jobs.
    """
    # NOTE: RecentlyPlayed is not a CRON job, it's triggered here to
    # populate the values for the very first time.
    RecentlyPlayed()
    RecentlyAdded()

    # Initialized CRON jobs
    # Mixes()
    TopArtists()
    TopArtists(duration="week")

    # Trigger all CRON jobs when the app is started.
    schedule.run_all()

    # Run all CRON jobs on a loop.
    while True:
        schedule.run_pending()
        time.sleep(1)
