from app.crons.cron import CronJob
from app.plugins.mixes import MixesPlugin
from app.store.homepage import HomepageStore


class Mixes(CronJob):
    """
    This cron job creates mixes displayed on the homepage.
    """

    def __init__(self):
        super().__init__("mixes", 1)

    def run(self):
        """
        Creates the artist mixes
        """
        print("⭐⭐⭐⭐ Mixes cron job running")
        mixes = MixesPlugin()

        if not mixes.enabled:
            return

        artist_mixes = mixes.create_artist_mixes()

        if artist_mixes:
            HomepageStore.set_artist_mixes(artist_mixes)
