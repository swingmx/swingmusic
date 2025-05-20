from dataclasses import dataclass


@dataclass
class StatItem:
    cssclass: str
    text: str
    value: str | int
    image: str | None = None
