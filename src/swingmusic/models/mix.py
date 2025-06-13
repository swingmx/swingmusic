import time
from dataclasses import asdict, dataclass, field
from typing import Any

from swingmusic.db.utils import row_to_dict
from swingmusic.lib.playlistlib import get_first_4_images
from swingmusic.serializers.track import serialize_tracks
from swingmusic.store.tracks import TrackStore
from swingmusic.utils.dates import seconds_to_time_string, timestamp_to_time_passed
from swingmusic.utils.hashing import create_hash


@dataclass
class Mix:
    id: str
    title: str
    description: str
    tracks: list[str]
    sourcehash: str
    userid: int
    """
    A hash of the tracks used to generate the mix.
    """

    timestamp: int = field(default_factory=lambda: int(time.time()))
    extra: dict = field(default_factory=dict)
    saved: bool = False

    def to_full_dict(self):
        tracks = TrackStore.get_tracks_by_trackhashes(self.tracks)[:40]
        serialized_tracks = serialize_tracks(tracks)

        _dict = asdict(self)
        _dict["tracks"] = serialized_tracks

        # if not self.extra.get("image"):
        #     _dict["images"] = get_first_4_images(tracks)

        _dict["duration"] = seconds_to_time_string(sum(t.duration for t in tracks))
        _dict["trackcount"] = len(tracks)

        del _dict["extra"]["albums"]
        del _dict["extra"]["artists"]

        return _dict

    def to_dict(self, convert_timestamp: bool = False):
        item = asdict(self)
        item["trackshash"] = create_hash(*self.tracks[:40])
        item["type"] = "mix"

        if convert_timestamp:
            item["time"] = timestamp_to_time_passed(item["timestamp"])

        del item["tracks"]

        del item["extra"]["albums"]
        del item["extra"]["artists"]

        return item

    @classmethod
    def mix_to_dataclass(cls, entry: Any):
        entry_dict = row_to_dict(entry)

        entry_dict["id"] = entry_dict["mixid"]
        del entry_dict["mixid"]

        return Mix(**entry_dict)

    @classmethod
    def mixes_to_dataclasses(cls, entries: Any):
        return [cls.mix_to_dataclass(entry) for entry in entries]
