from dataclasses import dataclass
from typing import Any, Literal


@dataclass
class Favorite:
    hash: str
    type: Literal["album", "track", "artist"]
    timestamp: int
    userid: int
    extra: dict[str, Any]

    def __post_init__(self):
        # remove the type prefix from the hash
        self.hash = self.hash.replace(f"{self.type}_", "")
