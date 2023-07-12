"""
Contains methods for reading and writing to the sqlite artists database.
"""

import json
from sqlite3 import Cursor

from .utils import SQLiteManager


class SQLiteArtistMethods:
    @staticmethod
    def insert_one_artist(cur: Cursor, artisthash: str, colors: list[str]):
        """
        Inserts a single artist into the database.
        """
        sql = """INSERT OR REPLACE INTO artists(
            artisthash,
            colors
            ) VALUES(?,?)
            """
        colors = json.dumps(colors)
        cur.execute(sql, (artisthash, colors))

    @staticmethod
    def get_all_artists(cur_: Cursor = None):
        """
        Get all artists from the database and return a generator of Artist objects
        """
        sql = """SELECT * FROM artists"""

        if not cur_:
            with SQLiteManager() as cur:
                cur.execute(sql)

                for artist in cur.fetchall():
                    yield artist

                cur.close()

        else:
            cur_.execute(sql)

            for artist in cur_.fetchall():
                yield artist

    @staticmethod
    def exists(artisthash: str, cur: Cursor = None):
        """
        Checks if an artist exists in the database.
        """
        sql = "SELECT COUNT(1) FROM artists WHERE artisthash = ?"

        def _exists(cur: Cursor):
            cur.execute(sql, (artisthash,))
            count = cur.fetchone()[0]

            return count != 0

        if cur:
            return _exists(cur)

        with SQLiteManager() as cur:
            return _exists(cur)
