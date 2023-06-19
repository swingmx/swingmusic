"""
Contains methods for reading and writing to the sqlite artists database.
"""

import json
from sqlite3 import Cursor

from .utils import SQLiteManager


class SQLiteArtistMethods:
    @staticmethod
    def insert_one_artist(cur: Cursor, artisthash: str, colors: str | list[str]):
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
        cur.close()

    @staticmethod
    def get_all_artists():
        """
        Get all artists from the database and return a generator of Artist objects
        """
        sql = """SELECT * FROM artists"""

        with SQLiteManager() as cur:
            cur.execute(sql)

            for artist in cur.fetchall():
                yield artist

            cur.close()
