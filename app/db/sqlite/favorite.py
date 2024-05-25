from datetime import datetime

from flask_jwt_extended import current_user
from app.models import FavType
from .utils import SQLiteManager


class SQLiteFavoriteMethods:
    """THis class contains methods for interacting with the favorites table."""

    @classmethod
    def check_is_favorite(cls, itemhash: str, fav_type: str):
        """
        Checks if an item is favorited.
        """
        userid = current_user["id"]

        sql = """SELECT * FROM favorites WHERE hash = ? AND type = ? AND userid = ?"""
        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, (itemhash, fav_type, userid))
            item = cur.fetchone()
            cur.close()
            return item is not None

    @classmethod
    def insert_one_favorite(cls, fav_type: str, fav_hash: str):
        """
        Inserts a single favorite into the database.
        """
        # try to find the favorite in the database, if it exists, don't insert it
        if cls.check_is_favorite(fav_hash, fav_type):
            return

        sql = """INSERT INTO favorites(type, hash, timestamp, userid) VALUES(?,?,?,?)"""
        current_timestamp = int(datetime.now().timestamp())
        with SQLiteManager(userdata_db=True) as cur:
            userid = current_user["id"]
            cur.execute(sql, (fav_type, fav_hash, current_timestamp, userid))
            cur.close()

    @classmethod
    def get_all(cls) -> list[tuple]:
        """
        Returns a list of all favorites.
        """
        sql = """SELECT * FROM favorites WHERE userid = ?"""
        with SQLiteManager(userdata_db=True) as cur:
            userid = current_user["id"]
            cur.execute(sql, (userid,))
            favs = cur.fetchall()
            cur.close()
            return [fav for fav in favs if fav[1] != ""]

    @classmethod
    def get_favorites(cls, fav_type: str, userid: int = None) -> list[tuple]:
        """
        Returns a list of favorite tracks.

        If userid is None, all favorites are returned.
        """
        sql = """SELECT * FROM favorites WHERE type = ?"""
        params = (fav_type,)

        if not userid:
            sql += " AND userid = ?"
            params = (fav_type, userid)

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, params)
            all_favs = cur.fetchall()
            cur.close()
            return all_favs

    @classmethod
    def get_fav_tracks(cls, userid: int = None) -> list[tuple]:
        """
        Returns a list of favorite tracks.
        """
        return cls.get_favorites(FavType.track, userid)

    @classmethod
    def get_fav_albums(cls) -> list[tuple]:
        """
        Returns a list of favorite albums.
        """
        userid = current_user["id"]
        return cls.get_favorites(FavType.album, userid)

    @classmethod
    def get_fav_artists(cls) -> list[tuple]:
        """
        Returns a list of favorite artists.
        """
        userid = current_user["id"]
        return cls.get_favorites(FavType.artist, userid)

    @classmethod
    def delete_favorite(cls, fav_type: str, fav_hash: str):
        """
        Deletes a favorite from the database.
        """
        sql = """DELETE FROM favorites WHERE hash = ? AND type = ? AND userid = ?"""

        with SQLiteManager(userdata_db=True) as cur:
            userid = current_user["id"]
            cur.execute(sql, (fav_hash, fav_type, userid))
            cur.close()

    @classmethod
    def get_track_count(cls) -> int:
        """
        Returns the number of favorite tracks.
        """
        sql = """SELECT COUNT(*) FROM favorites WHERE type = ? AND userid = ?"""

        with SQLiteManager(userdata_db=True) as cur:
            userid = current_user["id"]
            cur.execute(sql, (FavType.track, userid))
            count = cur.fetchone()[0]
            cur.close()
            return count
