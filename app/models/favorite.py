from dataclasses import dataclass
from typing import Any, Literal


@dataclass
class Favorite:
    hash: str
    type: Literal["album", "track", "artist"]
    timestamp: int
    userid: int
    extra: dict[str, Any]