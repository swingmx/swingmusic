from .utils import SQLiteManager
from app.models import FavType


class SQLiteFavoriteMethods:
    """THis class contains methods for interacting with the favorites table."""

    @classmethod
    def insert_one_favorite(cls, fav_type: str, fav_hash: str):
        """
        Inserts a single favorite into the database.
        """
        sql = """INSERT INTO favorites(type, hash) VALUES(?,?)"""
        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, (fav_type, fav_hash))

    @classmethod
    def get_all(cls) -> list[tuple]:
        """
        Returns a list of all favorites.
        """
        sql = """SELECT * FROM favorites"""
        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql)
            return cur.fetchall()

    @classmethod
    def get_favorites(cls, fav_type: str) -> list[tuple]:
        """
        Returns a list of favorite tracks.
        """
        sql = """SELECT * FROM favorites WHERE type = ?"""
        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, (fav_type, ))
            return cur.fetchall()

    @classmethod
    def get_fav_tracks(cls) -> list[tuple]:
        """
        Returns a list of favorite tracks.
        """
        return cls.get_favorites(FavType.track)

    @classmethod
    def get_fav_albums(cls) -> list[tuple]:
        """
        Returns a list of favorite albums.
        """
        return cls.get_favorites(FavType.album)

    @classmethod
    def get_fav_artists(cls) -> list[tuple]:
        """
        Returns a list of favorite artists.
        """
        return cls.get_favorites(FavType.artist)

    @classmethod
    def delete_favorite(cls, fav_type: str, fav_hash: str):
        """
        Deletes a favorite from the database.
        """
        sql = """DELETE FROM favorites WHERE hash = ? AND type = ?"""

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, (fav_hash, fav_type))

    @classmethod
    def check_is_favorite(cls, itemhash: str, fav_type: str):
        """
        Checks if an item is favorited.
        """
        sql = """SELECT * FROM favorites WHERE hash = ? AND type = ?"""
        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, (itemhash, fav_type))
            items = cur.fetchall()
            return len(items) > 0
