import pprint
from app.db.userdata import UserTable
from app.lib.home.recentlyadded import get_recently_added_items
from app.lib.home.recentlyplayed import get_recently_played
from app.lib.recipes import HomepageRoutine
from app.store.homepage import HomepageStore


class RecentlyPlayed(HomepageRoutine):
    store_key = "recently_played"

    def __init__(self, userid: int | None = None) -> None:
        """
        The userid is provided when we are running this routine
        outside a cron job. ie. when a user records a new scrobble.
        """
        self.userids = [userid] if userid else [user.id for user in UserTable.get_all()]
        super().__init__()

    @property
    def is_valid(self):
        return True

    def run(self):
        for userid in self.userids:
            items = get_recently_played(limit=15, userid=userid)
            HomepageStore.entries[self.store_key].items[userid] = items


class RecentlyAdded(HomepageRoutine):
    ITEM_LIMIT = 15
    store_key = "recently_added"

    @property
    def is_valid(self):
        return True

    def __init__(self):
        super().__init__()

    def run(self):
        items = get_recently_added_items(limit=self.ITEM_LIMIT)

        # NOTE: Recently added is a global entry
        # So we don't need a userid
        HomepageStore.entries[self.store_key].items[0] = items
