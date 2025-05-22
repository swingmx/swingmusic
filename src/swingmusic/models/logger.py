from dataclasses import dataclass
from typing import Any, Literal


@dataclass
class TrackLog:
    """
    Track play logger model
    """

    id: int
    trackhash: str
    duration: int
    timestamp: int
    source: str
    """
    The full source string, eg. "al:123456"
    """
    userid: int
    extra: dict[str, Any]

    type = "track"
    type_src = None
    """
    The source identifier string, eg. albumhash, artisthash, etc.
    """

    def __post_init__(self):
        prefix_map = {
            "mix:": "mix",
            "al:": "album",
            "ar:": "artist",
            "fo:": "folder",
            "pl:": "playlist",
            "favorite": "favorite",
        }

        for prefix, srctype in prefix_map.items():
            if self.source.startswith(prefix):
                try:
                    self.type_src = self.source.split(":", 1)[1]
                except IndexError:
                    self.type_src = None

                self.type = srctype
                break
