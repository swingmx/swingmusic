from abc import ABC
from typing import Any

from swingmusic.lib.home.recover_items import recover_items
from swingmusic.models.mix import Mix

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
            "items": recover_items(items),
        }


class RecentlyAddedHomepageEntry(RecentlyPlayedHomepageEntry):
    """
    A homepage entry for recently added.
    """

    def get_items(self, userid: int, limit: int | None = None):
        return super().get_items(0, limit)


class GenericRecoverableEntry(RecentlyPlayedHomepageEntry):
    """
    A homepage entry for top streamed.
    """

    # NOTE: This extends RecentlyPlayedHomepageEntry because
    # the shape of the data is the same.
    pass


class BecauseYouListenedToArtistHomepageEntry(RecentlyPlayedHomepageEntry):
    """
    A homepage entry for because you listened to artist.
    """

    # SHAPE: {userid: {title: str, items: list[RecoverableItem]}}
    items: dict[int, dict[str, Any]]

    def get_items(self, userid: int, limit: int | None = None):
        title = self.items.get(userid, {}).get("title")
        items = self.items.get(userid, {}).get("items", [])[:limit]

        return {
            "title": title,
            "items": recover_items(items),
        }

