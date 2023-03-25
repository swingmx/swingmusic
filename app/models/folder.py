from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Folder:
    name: str
    path: str
    is_sym: bool = False
    count: int = 0
