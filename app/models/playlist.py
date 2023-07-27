import dataclasses
import json
from dataclasses import dataclass
from pathlib import Path

from app import settings


@dataclass(slots=True)
class Playlist:
    """Creates playlist objects"""

    id: int
    artisthashes: str | list[str]
    image: str
    last_updated: str
    name: str
    settings: str | dict
    trackhashes: str | list[str]

    thumb: str = ""
    count: int = 0
    duration: int = 0
    has_image: bool = False
    images: list[str] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self.trackhashes = json.loads(str(self.trackhashes))
        # self.artisthashes = json.loads(str(self.artisthashes))
        # commentted until we need it 👆

        self.artisthashes = []

        self.count = len(self.trackhashes)

        if isinstance(self.settings, str):
            self.settings = json.loads(self.settings)

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

    def clear_lists(self):
        """
        Removes data from lists to make it lighter for sending
        over the API.
        """
        self.trackhashes = []
        self.artisthashes = []
