import dataclasses
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from swingmusic import settings
from swingmusic.utils.auth import get_current_userid


@dataclass(slots=True)
class Playlist:
    """Creates playlist objects"""

    id: int | str
    image: str | None
    last_updated: str
    name: str
    settings: dict
    trackhashes: list[str] = dataclasses.field(default_factory=list)
    extra: dict[str, Any] = dataclasses.field(default_factory=dict)

    _last_updated: str = ""
    userid: int | None = None
    thumb: str = ""
    count: int = 0
    duration: int = 0
    has_image: bool = False
    images: list[dict[str, str]] = dataclasses.field(default_factory=list)
    pinned: bool = False
    _score: float = 0
    def __post_init__(self):
        self.count = len(self.trackhashes)

        if self.userid is None:
            self.userid = get_current_userid()

        self.pinned = self.settings.get("pinned", False)
        self.has_image = (
            Path(settings.Paths.get_playlist_img_path()) / str(self.image)
        ).exists()

        if self.image is not None:
            self.thumb = "thumb_" + self.image
        else:
            self.image = "None"
            self.thumb = "None"

    def clear_lists(self):
        """
        Removes data from lists to make it lighter for sending
        over the API.
        """
        self.trackhashes = []
