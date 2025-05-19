from typing import Any

from swingmusic.db.userdata import CollectionTable
from swingmusic.lib.pagelib import recover_page_items
from swingmusic.store.homepageentries import (
    BecauseYouListenedToArtistHomepageEntry,
    GenericRecoverableEntry,
    HomepageEntry,
    MixHomepageEntry,
    RecentlyAddedHomepageEntry,
    RecentlyPlayedHomepageEntry,
)
from swingmusic.utils.auth import get_current_userid


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
        "custom_mixes": MixHomepageEntry(
            title="Mixes for you",
            description="Because artist mixes alone aren't enough",
        ),
        "top_streamed_weekly_artists": GenericRecoverableEntry(
            title="Top artists this week",
            description="Your most played artists since Monday",
        ),
        "top_streamed_monthly_artists": GenericRecoverableEntry(
            title="Top artists this month",
            description="Your most played artists since the start of the month",
        ),
        "because_you_listened_to_artist": BecauseYouListenedToArtistHomepageEntry(
            title="",
            description="Artists similar to the artist you listened to",
        ),
        "artists_you_might_like": BecauseYouListenedToArtistHomepageEntry(
            title="Artists you might like",
            description="Artists similar to the artists you have listened to",
        ),
        "recently_added": RecentlyAddedHomepageEntry(
            title="Recently added",
            description="New music added to your library",
        ),
    }

    @classmethod
    def set_mixes(cls, items: list[Any], entrykey: str, userid: int | None = None):
        idmap = {item.id: item for item in items}
        cls.entries[entrykey].items[userid or get_current_userid()] = idmap

    @classmethod
    def get_mix(cls, mixkey: str, mixid: str):
        mix = cls.entries[mixkey].items.get(get_current_userid(), {}).get(mixid)
        return mix.to_full_dict() if mix else None

    @classmethod
    def get_homepage_items(cls, limit: int):
        # return a dict of entry name to entry items
        pages = CollectionTable.get_all()
        pagedata = []

        for page in pages:
            pagedata.append(
                {
                    page["id"]: {
                        "id": page["id"],
                        "title": page["name"],
                        "description": page["extra"]["description"],
                        "items": recover_page_items(page["items"], for_homepage=True),
                        "url": f"collections/{page['id']}",
                    }
                }
            )

        homedata = [
            {entry: cls.entries[entry].get_items(get_current_userid(), limit)}
            for entry in cls.entries.keys()
            if len(cls.entries[entry].items)
        ]

        recently_added = homedata.pop()
        return homedata + pagedata + [recently_added]

    @classmethod
    def find_mix(cls, mixid: str):
        mixentries = ["artist_mixes", "custom_mixes"]

        for entry in mixentries:
            mix = cls.entries[entry].items.get(get_current_userid(), {}).get(mixid)
            if mix:
                return mix

        return None
