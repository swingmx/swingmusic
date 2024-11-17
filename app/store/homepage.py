from abc import ABC
from dataclasses import dataclass
from typing import Any
from app.lib.home.recentlyplayed import recover_recently_played_items
from app.models.mix import Mix
from app.utils.auth import get_current_userid


class HomepageEntry(ABC):
    """
    Base class for all homepage entries.

    items is a dict of userid to a dict of stuff.
    """

    title: str
    description: str
    items: dict[int, Any]

    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description

    def get_items(self, userid: int, limit: int | None = None):
        """
        Return usable items for the homepage.
        """
        ...


class MixHomepageEntry(HomepageEntry):
    """
    A homepage entry for mixes.
    self.items is a dict of userid to a dict of mixid to mix.
    """

    items: dict[int, dict[str, Mix]]

    def __init__(self, title: str, description: str):
        super().__init__(title, description)
        self.items = {}

    def get_items(self, userid: int, limit: int | None = None):
        items = []

        for mix in self.items.get(userid, {}).values():
            if limit and len(items) >= limit:
                break

            items.append(
                {
                    "type": "mix",
                    "item": mix.to_dict(),
                }
            )

        return {
            "title": self.title,
            "description": self.description,
            "items": items,
        }


class RecentlyPlayedHomepageEntry(HomepageEntry):
    """
    A homepage entry for recently played.
    """

    items: dict[int, list[dict[str, Any]]]

    def __init__(self, title: str, description: str = ""):
        super().__init__(title, description)
        self.items = {}

    def get_items(self, userid: int, limit: int | None = None):
        items = self.items.get(userid, [])[:limit]

        return {
            "title": self.title,
            "description": self.description,
            "items": recover_recently_played_items(items),
        }


class RecentlyAddedHomepageEntry(RecentlyPlayedHomepageEntry):
    """
    A homepage entry for recently added.
    """

    def get_items(self, userid: int, limit: int | None = None):
        return super().get_items(0, limit)


class TopStreamedHomepageEntry(RecentlyPlayedHomepageEntry):
    """
    A homepage entry for top streamed.
    """

    # NOTE: This extends RecentlyPlayedHomepageEntry because
    # the shape of the data is the same.
    pass


class HomepageStore:
    """
    Stores the homepage items.
    """

    entries: dict[str, HomepageEntry] = {
        "recently_played": RecentlyPlayedHomepageEntry(
            title="Recently played",
        ),
        "artist_mixes": MixHomepageEntry(
            title="Artist mixes for you",
            description="Based on artists you have been listening to",
        ),
        "top_streamed_weekly_artists": TopStreamedHomepageEntry(
            title="Top artists this week",
            description="Your most played artists since Monday",
        ),
        "top_streamed_monthly_artists": TopStreamedHomepageEntry(
            title="Top artists this month",
            description="Your most played artists since the start of the month",
        ),
        "recently_added": RecentlyAddedHomepageEntry(
            title="Recently added",
            description="New music added to your library",
        ),
    }

    @classmethod
    def set_mixes(cls, items: list[Any], entrykey: str, userid: int | None = None):
        idmap = {item.id[1:]: item for item in items}
        cls.entries[entrykey].items[userid or get_current_userid()] = idmap

    @classmethod
    def get_mix(cls, mixkey: str, mixid: str):
        mix = cls.entries[mixkey].items.get(get_current_userid(), {}).get(mixid)
        return mix.to_full_dict() if mix else None

    @classmethod
    def get_homepage_items(cls, limit: int):
        # return a dict of entry name to entry items
        return [
            {entry: cls.entries[entry].get_items(get_current_userid(), limit)}
            for entry in cls.entries.keys()
            if len(cls.entries[entry].items)
        ]
