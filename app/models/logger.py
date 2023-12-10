from dataclasses import dataclass
from typing import Literal


@dataclass
class Track:
    """
    Track play logger model
    """

    id: int
    trackhash: str
    duration: int
    timestamp: int
    source: str
    userid: int

    type = "track"
    type_src = None

    def __post_init__(self):
        prefix_map = {
            "al:": "album",
            "ar:": "artist",
            "pl:": "playlist",
            "fo:": "folder",
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
