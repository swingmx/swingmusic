from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Folder:
    name: str
    path: str
    is_sym: bool = False
    trackcount: int = 0
