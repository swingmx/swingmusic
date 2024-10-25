from dataclasses import asdict, dataclass, field
import time

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

    timestamp: int = field(default_factory=lambda: int(time.time()))
    extra: dict = field(default_factory=dict)
    saved: bool = False

    def to_full_dict(self):
        tracks = TrackStore.get_tracks_by_trackhashes(self.tracks)
        serialized_tracks = serialize_tracks(tracks)

        _dict = asdict(self)
        _dict["tracks"] = serialized_tracks
        _dict["images"] = get_first_4_images(tracks)
        _dict["duration"] = seconds_to_time_string(sum(t.duration for t in tracks))
        _dict["trackcount"] = len(tracks)

        return _dict

    def to_dict(self):
        item = self.to_full_dict()
        del item["tracks"]

        return item
