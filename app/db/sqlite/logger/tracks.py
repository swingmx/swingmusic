from app.db.sqlite.utils import SQLiteManager


class SQLiteTrackLogger:
    @classmethod
    def insert_track(cls, trackhash: str, duration: int, source: str, timestamp: int):
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
