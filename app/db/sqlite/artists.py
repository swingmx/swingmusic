"""
Contains methods for reading and writing to the sqlite artists database.
"""
import json

from .utils import SQLiteManager


class SQLiteArtistMethods:

    @classmethod
    def insert_one_artist(cls, artisthash: str, colors: str | list[str]):
        """
        Inserts a single artist into the database.
        """
        sql = """INSERT INTO artists(
            artisthash,
            colors
            ) VALUES(?,?)
            """
        colors = json.dumps(colors)

        with SQLiteManager() as cur:
            cur.execute(sql, (artisthash, colors))

    @classmethod
    def get_all_artists(cls):
        """
        Get all artists from the database and return a generator of Artist objects
        """
        sql = """SELECT * FROM artists"""

        with SQLiteManager() as cur:
            cur.execute(sql)

            for artist in cur.fetchall():
                yield artist
