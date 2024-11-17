from app.crons.cron import CronJob
from app.lib.recipes.artistmixes import ArtistMixes


class Mixes(CronJob):
    """
    This cron job creates mixes displayed on the homepage.
    """

    name: str = "mixes"
    hours: int = 6

    def __init__(self):
        super().__init__()

    def run(self):
        """
        Creates the artist mixes
        """
        print("⭐⭐⭐⭐ Mixes cron job running")
        ArtistMixes()
