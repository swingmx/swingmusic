from dataclasses import dataclass


@dataclass
class Plugin:
    name: str
    active: bool
    settings: dict
    extra: dict

