import pprint
from app.db.userdata import ScrobbleTable, UserTable
from app.lib.home.recentlyadded import get_recently_added_items
from app.lib.home.get_recently_played import get_recently_played
from app.lib.recipes import HomepageRoutine
from app.store.homepage import HomepageStore


class RecentlyPlayed(HomepageRoutine):
    ITEM_LIMIT = 15
    store_key = "recently_played"

    def __init__(self, userid: int | None = None) -> None:
        """
        The userid is provided when we are running this routine
        outside a cron job. ie. when a user records a new scrobble.
        """
        self.userids = [userid] if userid else [user.id for user in UserTable.get_all()]

        # NOTE: When the userid is provided
        # we need to update the store for that userid only
        # using the last scrobble entry.
        self.update_only = userid is not None
        super().__init__()

    @property
    def is_valid(self):
        return True

    def run(self):
        if self.update_only:
            last_entry = ScrobbleTable.get_last_entry(self.userids[0])

            if last_entry:
                items = get_recently_played(
                    limit=self.ITEM_LIMIT, userid=self.userids[0], _entries=[last_entry]
                )

                item = items[0]
                try:
                    store_entry = HomepageStore.entries[self.store_key].items[
                        self.userids[0]
                    ][0]
                except IndexError:
                    store_entry = None

                if (
                    store_entry and item["type"] + item["hash"]
                    == store_entry["type"] + store_entry["hash"]
                ):
                    # If the item is the same as the one in the store
                    # only update the timestamp
                    HomepageStore.entries[self.store_key].items[self.userids[0]][0][
                        "timestamp"
                    ] = item["timestamp"]
                else:
                    # Otherwise, insert the new item
                    # and remove the oldest item if there are more than 15 items
                    HomepageStore.entries[self.store_key].items[self.userids[0]].insert(
                        0, item
                    )

                    if (
                        len(
                            HomepageStore.entries[self.store_key].items[self.userids[0]]
                        )
                        > self.ITEM_LIMIT
                    ):
                        HomepageStore.entries[self.store_key].items[
                            self.userids[0]
                        ].pop()

        for userid in self.userids:
            items = get_recently_played(limit=self.ITEM_LIMIT, userid=userid)
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
