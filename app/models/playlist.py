import dataclasses
import json
from dataclasses import dataclass
from pathlib import Path

from app import settings


@dataclass(slots=True)
class Playlist:
    """Creates playlist objects"""

    id: int
    image: str | None
    last_updated: str
    name: str
    settings: str | dict
    trackhashes: str | list[str]

    thumb: str | None = ""
    count: int = 0
    duration: int = 0
    has_image: bool = False
    images: list[str] = dataclasses.field(default_factory=list)
    pinned: bool = False

    def __post_init__(self):
        self.trackhashes = json.loads(str(self.trackhashes))
        self.count = len(self.trackhashes)

        if isinstance(self.settings, str):
            self.settings = dict(json.loads(self.settings))

        self.pinned = self.settings.get("pinned", False)
        self.has_image = (
            Path(settings.Paths.get_playlist_img_path()) / str(self.image)
        ).exists()

        if self.image is not None:
            self.thumb = "thumb_" + self.image
        else:
            self.image = "None"
            self.thumb = "None"

    def set_duration(self, duration: int):
        self.duration = duration

    def set_count(self, count: int):
        self.count = count

    def clear_lists(self):
        """
        Removes data from lists to make it lighter for sending
        over the API.
        """
        self.trackhashes = []
