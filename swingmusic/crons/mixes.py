from swingmusic.crons.cron import CronJob
from swingmusic.lib.recipes.artistmixes import ArtistMixes
from swingmusic.lib.recipes.because import BecauseYouListened


class Mixes(CronJob):
    """
    This cron job creates mixes displayed on the homepage.
    """

    name: str = "mixes"
    hours: int = 12

    def __init__(self):
        super().__init__()

    def run(self):
        """
        Creates the artist mixes
        """
        ArtistMixes()

        # INFO: Because you listened to artist items are generated using
        # the artist mixes, so run them after the artist mixes are created.
        BecauseYouListened()
