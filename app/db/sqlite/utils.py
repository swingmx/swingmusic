"""
Helper functions for use with the SQLite database.
"""

import sqlite3
from sqlite3 import Connection, Cursor

from app.models import Album, Playlist, Track
from app.settings import APP_DB_PATH, USERDATA_DB_PATH


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

    def __init__(self, conn: Connection | None = None, userdata_db=False) -> None:
        """
        When a connection is passed in, don't close the connection, because it's
        a connection to the search database [in memory db].
        """
        self.conn: Connection | None = conn
        self.CLOSE_CONN = True
        self.userdata_db = userdata_db

        if conn:
            self.conn = conn
            self.CLOSE_CONN = False

    def __enter__(self) -> Cursor:
        if self.conn is not None:
            return self.conn.cursor()

        db_path = APP_DB_PATH

        if self.userdata_db:
            db_path = USERDATA_DB_PATH

        self.conn = sqlite3.connect(db_path)
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.conn:
            self.conn.commit()

            if self.CLOSE_CONN:
                self.conn.close()
