"""
Helper functions for use with the SQLite database.
"""

import sqlite3
from sqlite3 import Connection, Cursor
import time
from typing import Optional

from app.models import Album, Playlist, Track
from app import settings


def tuple_to_track(track: tuple):
    """
    Takes a tuple and returns a Track object
    """
    return Track(*track[1:])  # rowid is removed from the tuple


def tuples_to_tracks(tracks: list[tuple]):
    """
    Takes a list of tuples and returns a generator that yields a Track object for each tuple
    """
    for track in tracks:
        yield tuple_to_track(track)


def tuple_to_album(album: tuple):
    """
    Takes a tuple and returns an Album object
    """
    return Album(*album[1:])  # rowid is removed from the tuple


def tuples_to_albums(albums: list[tuple]):
    """
    Takes a list of tuples and returns a generator that yields an album object for each tuple
    """
    for album in albums:
        yield tuple_to_album(album)


def tuple_to_playlist(playlist: tuple):
    """
    Takes a tuple and returns a Playlist object
    """
    return Playlist(*playlist)


def tuples_to_playlists(playlists: list[tuple]):
    """
    Takes a list of tuples and returns a list of Playlist objects
    """
    for playlist in playlists:
        yield tuple_to_playlist(playlist)


class SQLiteManager:
    """
    This is a context manager that handles the connection and cursor
    for you. It also commits and closes the connection when you're done.
    """

    def __init__(
        self,
        conn: Optional[Connection] = None,
        userdata_db=False,
        test_db_path: str = None,
    ) -> None:
        """
        When a connection is passed in, don't close the connection, because it's
        a connection to the search database [in memory db].
        """
        self.conn = conn
        self.CLOSE_CONN = True
        self.userdata_db = userdata_db
        self.test_db_path = test_db_path

        if conn:
            self.conn = conn
            self.CLOSE_CONN = False

    def __enter__(self) -> Cursor:
        if self.conn is not None:
            return self.conn.cursor()

        if self.test_db_path:
            db_path = self.test_db_path
        else:
            db_path = settings.Db.get_app_db_path()

        if self.userdata_db:
            db_path = settings.Db.get_userdata_db_path()

        self.conn = sqlite3.connect(
            db_path,
            timeout=15,
        )
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        trial_count = 0

        while trial_count < 10:
            try:
                self.conn.commit()

                if self.CLOSE_CONN:
                    self.conn.close()

                return
            except sqlite3.OperationalError:
                trial_count += 1
                time.sleep(3)

        self.conn.close()
