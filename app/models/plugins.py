from dataclasses import dataclass


@dataclass
class Plugin:
    name: str
    description: str
    active: bool
    settings: dict

