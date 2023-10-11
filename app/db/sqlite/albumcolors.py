from sqlite3 import Cursor

from .utils import SQLiteManager, tuples_to_albums


class SQLiteAlbumMethods:
    @classmethod
    def insert_one_album(cls, cur: Cursor, albumhash: str, colors: str):
        """
        Inserts one album into the database
        """

        sql = """INSERT OR REPLACE INTO albums(
            albumhash,
            colors
            ) VALUES(?,?)
            """

        cur.execute(sql, (albumhash, colors))
        lastrowid = cur.lastrowid

        return lastrowid

    @classmethod
    def get_all_albums(cls):
        with SQLiteManager() as cur:
            cur.execute("SELECT * FROM albums")
            albums = cur.fetchall()
            cur.close()

            if albums is not None:
                return albums

        return []

    @staticmethod
    def get_albums_by_albumartist(albumartist: str):
        with SQLiteManager() as cur:
            cur.execute("SELECT * FROM albums WHERE albumartist=?", (albumartist,))
            albums = cur.fetchall()
            cur.close()

            if albums is not None:
                return tuples_to_albums(albums)

        return []

    @staticmethod
    def exists(albumhash: str, cur: Cursor = None):
        """
        Checks if an album exists in the database.
        """

        sql = "SELECT COUNT(1) FROM albums WHERE albumhash = ?"

        def _exists(cur: Cursor):
            cur.execute(sql, (albumhash,))
            count = cur.fetchone()[0]

            return count != 0

        if cur:
            return _exists(cur)

        with SQLiteManager() as cur:
            return _exists(cur)
