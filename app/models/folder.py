from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Folder:
    name: str
    path: str
    has_tracks: bool
    is_sym: bool = False
    path_hash: str = ""
