from gettext import ngettext
import pendulum

from swingmusic.crons.cron import CronJob
from swingmusic.db.userdata import UserTable
from swingmusic.lib.recipes import HomepageRoutine
from swingmusic.store.homepage import HomepageStore
from swingmusic.utils.dates import get_date_range, seconds_to_time_string
from swingmusic.utils.stats import get_artists_in_period


class TopArtists(CronJob, HomepageRoutine):
    """
    A routine to populate the top streamed artists/albums in the last week or month
    """

    hours = 1
    ITEM_LIMIT = 15

    @property
    def is_valid(self):
        """
        Only valid if it's the middle or last 2 days of this month.

        When the duration is "week", it's valid on the weekend.
        """
        if self.duration == "month":
            now = pendulum.now()
            middle_day = now.days_in_month // 2

            return (
                now.day in range(middle_day, middle_day + 2)
                or now.day > now.days_in_month - 2
            )
        if self.duration == "week":
            return pendulum.now().isoweekday() in (5, 6, 7)

        return False

    def __init__(self, duration: str = "month") -> None:
        super().__init__()
        self.duration = duration

        if not self.is_valid:
            return

    def run(self):
        if not self.is_valid:
            self.destroy()
            return

        self.userids = [user.id for user in UserTable.get_all()]

        for userid in self.userids:
            date_range = get_date_range(self.duration)
            artists = get_artists_in_period(date_range[0], date_range[1], userid)[
                : self.ITEM_LIMIT
            ]

            artists = [
                {
                    "type": "artist",
                    "hash": artist["artisthash"],
                    "help_text": seconds_to_time_string(artist["playduration"]),
                    "secondary_text": str(artist["playcount"])
                    + " "
                    + ngettext("play", "plays", artist["playcount"]),
                }
                for artist in artists
            ]

            HomepageStore.entries[f"top_streamed_{self.duration}ly_artists"].items[
                userid
            ] = artists

    def destroy(self):
        """
        Clear the top streamed entry from the homepage store.
        """
        keys = [f"top_streamed_{self.duration}ly_artists"]

        for key in keys:
            HomepageStore.entries[key].items = {}
