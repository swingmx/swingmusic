from dataclasses import dataclass
from app import models


@dataclass
class Playlist:
    playlistid: str
    name: str
    image: str
    lastUpdated: int
    description: str
    count: int = 0

    def __init__(self, p: models.Playlist) -> None:
        self.playlistid = p.playlistid
        self.name = p.name
        self.image = p.image
        self.lastUpdated = p.lastUpdated
        self.description = p.description
        self.count = p.count
