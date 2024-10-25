from app.crons.cron import CronJob
from app.plugins.mixes import MixesPlugin
from app.store.homepage import HomepageStore


class Mixes(CronJob):
    def __init__(self):
        super().__init__("mixes", 5)

    def run(self):
        print("⭐⭐⭐⭐ Mixes cron job running")
        mixes = MixesPlugin()
        artist_mixes = mixes.get_artists()

        HomepageStore.set_artist_mixes(artist_mixes)
