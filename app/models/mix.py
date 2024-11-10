import time
from dataclasses import asdict, dataclass, field
from typing import Any

from app.lib.playlistlib import get_first_4_images
from app.serializers.track import serialize_tracks
from app.store.tracks import TrackStore
from app.utils.dates import seconds_to_time_string


@dataclass
class Mix:
    id: str
    title: str
    description: str
    tracks: list[str]
    sourcehash: str
    """
    A hash of the tracks used to generate the mix.
    """

    timestamp: int = field(default_factory=lambda: int(time.time()))
    extra: dict = field(default_factory=dict)
    saved: bool = False

    def to_full_dict(self):
        # Limit track mix to 30 tracks
        tracks = TrackStore.get_tracks_by_trackhashes(self.tracks)
        serialized_tracks = serialize_tracks(tracks)

        _dict = asdict(self)
        _dict["tracks"] = serialized_tracks

        if not self.extra.get("image"):
            _dict["images"] = get_first_4_images(tracks)

        _dict["duration"] = seconds_to_time_string(sum(t.duration for t in tracks))
        _dict["trackcount"] = len(tracks)

        return _dict

    def to_dict(self):
        item = asdict(self)
        del item["tracks"]

        return item

    @classmethod
    def mix_to_dataclass(cls, entry: Any):
        entry_dict = entry._asdict()
        entry_dict["id"] = entry_dict["mixid"]
        del entry_dict["mixid"]

        return Mix(**entry_dict)

    @classmethod
    def mixes_to_dataclasses(cls, entries: Any):
        return [cls.mix_to_dataclass(entry) for entry in entries]
