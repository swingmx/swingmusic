from dataclasses import dataclass
from datetime import datetime

from app import models


def date_string_to_time_passed(prev_date: str) -> str:
    """
    Converts a date string to time passed. eg. 2 minutes ago, 1 hour ago, yesterday, 2 days ago, 2 weeks ago, etc.
    """

    now = datetime.now()
    then = datetime.strptime(prev_date, "%Y-%m-%d %H:%M:%S")

    diff = now - then
    days = diff.days

    if days < 0:
        return "in the future"

    elif days == 0:
        seconds = diff.seconds
        if seconds < 15:
            return "now"
        elif seconds < 60:
            return str(seconds) + " seconds ago"
        elif seconds < 3600:
            return str(seconds // 60) + " minutes ago"
        else:
            return str(seconds // 3600) + " hours ago"

    elif days == 1:
        return "yesterday"
    elif days < 7:
        return str(days) + " days ago"
    elif days < 30:
        if days < 14:
            return "1 week ago"

        return str(days // 7) + " weeks ago"
    elif days < 365:
        if days < 60:
            return "1 month ago"

        return str(days // 30) + " months ago"
    elif days > 365:
        if days < 730:
            return "1 year ago"

        return str(days // 365) + " years ago"


@dataclass
class Playlist:
    playlistid: str
    name: str
    image: str
    thumb: str
    lastUpdated: int
    description: str
    count: int = 0
    duration: int = 0

    def __init__(self,
                 p: models.Playlist,
                 construct_last_updated: bool = True) -> None:
        self.playlistid = p.playlistid
        self.name = p.name
        self.image = p.image
        self.thumb = p.thumb
        self.lastUpdated = p.lastUpdated
        self.description = p.description
        self.count = p.count

        if construct_last_updated:
            self.lastUpdated = self.get_l_updated(p.lastUpdated)

    @staticmethod
    def get_l_updated(date: str) -> str:
        return date_string_to_time_passed(date)
