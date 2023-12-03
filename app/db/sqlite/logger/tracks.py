from app.db.sqlite.utils import SQLiteManager
import time


class SQLiteTrackLogger:
    @classmethod
    def insert_track(cls, trackhash: str, duration: int, source: str):
        """
        Inserts a track into the database
        """

        with SQLiteManager(userdata_db=True) as cur:
            sql = """INSERT OR REPLACE INTO track_logger(
                trackhash,
                duration,
                timestamp,
                source,
                userid
                ) VALUES(?,?,?,?,?)
                """
            timestamp = int(time.time())

            cur.execute(sql, (trackhash, duration, timestamp, source, 0))
            lastrowid = cur.lastrowid

            return lastrowid

    @classmethod
    def get_all(cls):
        """
        Returns all tracks from the database
        """

        with SQLiteManager(userdata_db=True) as cur:
            sql = """SELECT * FROM track_logger ORDER BY timestamp DESC"""

            cur.execute(sql)
            rows = cur.fetchall()

            return rows
