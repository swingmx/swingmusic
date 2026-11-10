"""
Per-user play stats for tracks, albums and artists.
"""

import math
from dataclasses import dataclass
from typing import Iterable, Literal

ItemType = Literal["track", "album", "artist"]


@dataclass(slots=True)
class PlayStats:
    playcount: int = 0
    playduration: int = 0
    lastplayed: int = 0

    def add(self, duration: int, timestamp: int, playcount: int = 1):
        self.playcount += playcount
        self.playduration += duration
        self.lastplayed = max(self.lastplayed, timestamp)


def split_playcount(duration: int, track_duration: int) -> int:
    """
    The number of plays a logged duration counts as: one per started loop
    of the track, and at least one.
    """
    if track_duration <= 0:
        return 1
    return max(1, math.ceil(duration / track_duration))


# returned for unplayed items; never mutated
NO_PLAYS = PlayStats()


class PlayStore:
    """
    Play stats keyed by user, item type and item hash.
    """

    stats: dict[int, dict[ItemType, dict[str, PlayStats]]] = {}

    @classmethod
    def clear(cls):
        cls.stats = {}

    @classmethod
    def of(cls, userid: int, itemtype: ItemType) -> dict[str, PlayStats]:
        """
        Returns a user's stats for one item type, keyed by item hash.
        """
        return cls.stats.get(userid, {}).get(itemtype, {})

    @classmethod
    def get(cls, userid: int, itemtype: ItemType, itemhash: str) -> PlayStats:
        return cls.of(userid, itemtype).get(itemhash, NO_PLAYS)

    @classmethod
    def durations(cls, userid: int, itemtype: ItemType) -> dict[str, int]:
        """
        Returns a user's play duration per item hash of one item type.
        """
        return {h: stats.playduration for h, stats in cls.of(userid, itemtype).items()}

    @classmethod
    def record(
        cls,
        userid: int,
        trackhash: str,
        albumhash: str,
        artisthashes: Iterable[str],
        duration: int,
        timestamp: int,
        playcount: int = 1,
    ):
        """
        Adds plays of a track to the user's stats for the track, its album and its artists.
        """
        user = cls.stats.setdefault(userid, {})
        items = [("track", trackhash), ("album", albumhash)]
        items += [("artist", artisthash) for artisthash in dict.fromkeys(artisthashes)]

        for itemtype, itemhash in items:
            user.setdefault(itemtype, {}).setdefault(itemhash, PlayStats()).add(
                duration, timestamp, playcount
            )
