from app.db.sqlite.utils import SQLiteManager
from app.models.logger import TrackLog as TrackLog


class SQLiteTrackLogger:
    @classmethod
    def insert_track(cls, trackhash: str, duration: int, source: str, timestamp: int, userid: int):
        """
        Inserts a track play record into the database
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

            cur.execute(sql, (trackhash, duration, timestamp, source, userid))
            lastrowid = cur.lastrowid

            return lastrowid

    @classmethod
    def get_all(cls):
        """
        Returns all track play records from the database
        """

        with SQLiteManager(userdata_db=True) as cur:
            sql = """SELECT * FROM track_logger ORDER BY timestamp DESC"""

            cur.execute(sql)
            rows = cur.fetchall()

            return rows

    @classmethod
    def get_recently_played(cls, start: int = 0, limit: int = 100):
        """
        Returns a list of recently played tracks
        """

        with SQLiteManager(userdata_db=True) as cur:
            sql = """SELECT * FROM track_logger ORDER BY timestamp DESC LIMIT ?,?"""

            cur.execute(sql, (start, limit))
            rows = cur.fetchall()

            return [TrackLog(*row) for row in rows]