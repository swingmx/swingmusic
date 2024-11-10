from abc import ABC
from dataclasses import dataclass
from typing import Any
from app.models.mix import Mix
from app.utils.auth import get_current_userid


@dataclass
class HomepageEntry(ABC):
    """
    Base class for all homepage entries.

    items is a dict of userid to a dict of stuff.
    """

    title: str
    description: str
    items: dict[int, dict[str, Any]]

    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description

    def get_items(self, userid: int):
        """
        Return usable items for the homepage.
        """
        ...


@dataclass
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


class HomepageStore:
    """
    Stores the homepage items.
    """

    entries = {
        "artist_mixes": MixHomepageEntry(
            title="Artist mixes for you",
            description="Based on artists you have been listening to",
        ),
    }

    @classmethod
    def set_mixes(cls, mixes: list[Mix], mixkey: str, userid: int | None = None):
        idmap = {mix.id[1:]: mix for mix in mixes}
        cls.entries[mixkey].items[userid or get_current_userid()] = idmap

    @classmethod
    def get_mixes(cls, mixkey: str, limit: int | None = 9):
        return cls.entries[mixkey].get_items(get_current_userid(), limit)

    @classmethod
    def get_mix(cls, mixkey: str, mixid: str):
        mix = cls.entries[mixkey].items.get(get_current_userid(), {}).get(mixid)
        return mix.to_full_dict() if mix else None

    @classmethod
    def get_mix_by_sourcehash(cls, sourcehash: str):
        return next(
            (
                mix
                for mix in cls.entries["artist_mixes"]
                .items.get(get_current_userid(), {})
                .values()
                if mix.sourcehash == sourcehash
            ),
            None,
        )
