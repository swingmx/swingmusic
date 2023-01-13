"""
Contains the SQLiteTrackMethods class which contains methods for
interacting with the tracks table.
"""
from sqlite3 import Cursor

from .utils import SQLiteManager
from app.db.sqlite.utils import tuple_to_track
from app.db.sqlite.utils import tuples_to_tracks


class SQLiteTrackMethods:
    """
    This class contains all methods for interacting with the tracks table.
    """

    @classmethod
    def insert_one_track(cls, track: dict, cur: Cursor):
        """
        Inserts a single track into the database.
        """
        sql = """INSERT INTO tracks(
            album,
            albumartist,
            albumhash,
            artist,
            bitrate,
            copyright,
            date,
            disc,
            duration,
            filepath,
            folder,
            genre,
            title,
            track,
            trackhash
            ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """

        cur.execute(
            sql,
            (
                track["album"],
                track["albumartist"],
                track["albumhash"],
                track["artist"],
                track["bitrate"],
                track["copyright"],
                track["date"],
                track["disc"],
                track["duration"],
                track["filepath"],
                track["folder"],
                track["genre"],
                track["title"],
                track["track"],
                track["trackhash"],
            ),
        )

    @classmethod
    def insert_many_tracks(cls, tracks: list[dict]):
        """
        Inserts a list of tracks into the database.
        """
        with SQLiteManager() as cur:
            for track in tracks:
                cls.insert_one_track(track, cur)

    @staticmethod
    def get_all_tracks():
        """
        Get all tracks from the database and return a generator of Track objects
        or an empty list.
        """
        with SQLiteManager() as cur:
            cur.execute("SELECT * FROM tracks")
            rows = cur.fetchall()

            if rows is not None:
                return tuples_to_tracks(rows)

            return []

    @staticmethod
    def get_track_by_trackhash(trackhash: str):
        """
        Gets a track using its trackhash. Returns a Track object or None.
        """
        with SQLiteManager() as cur:
            cur.execute("SELECT * FROM tracks WHERE trackhash=?",
                        (trackhash, ))
            row = cur.fetchone()

            if row is not None:
                return tuple_to_track(row)

            return None

    @staticmethod
    def get_tracks_by_trackhashes(hashes: list[str]):
        """
        Gets all tracks in a list of trackhashes.
        Returns a generator of Track objects or an empty list.
        """

        sql = "SELECT * FROM tracks WHERE trackhash IN ({})".format(",".join(
            "?" * len(hashes)))

        with SQLiteManager() as cur:
            cur.execute(sql, hashes)
            rows = cur.fetchall()

            if rows is not None:
                return tuples_to_tracks(rows)

            return []

    @staticmethod
    def remove_track_by_filepath(filepath: str):
        """
        Removes a track from the database using its filepath.
        """
        with SQLiteManager() as cur:
            cur.execute("DELETE FROM tracks WHERE filepath=?", (filepath, ))

    @staticmethod
    def track_exists(filepath: str):
        """
        Checks if a track exists in the database using its filepath.
        """
        with SQLiteManager() as cur:
            cur.execute("SELECT * FROM tracks WHERE filepath=?", (filepath, ))
            row = cur.fetchone()

            if row is not None:
                return True

            return False
