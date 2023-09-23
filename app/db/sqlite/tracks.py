"""
Contains the SQLiteTrackMethods class which contains methods for
interacting with the tracks table.
"""

from collections import OrderedDict
from sqlite3 import Cursor

from app.db.sqlite.utils import tuple_to_track, tuples_to_tracks

from .utils import SQLiteManager
from pprint import pprint


class SQLiteTrackMethods:
    """
    This class contains all methods for interacting with the tracks table.
    """

    @classmethod
    def insert_one_track(cls, track: dict, cur: Cursor):
        """
        Inserts a single track into the database.
        """
        sql = """INSERT OR REPLACE INTO tracks(
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
            last_mod,
            title,
            track,
            trackhash
            ) VALUES(:album, :albumartist, :albumhash, :artist, :bitrate, :copyright, 
            :date, :disc, :duration, :filepath, :folder, :genre, :last_mod, :title, :track, :trackhash)
            """

        track = OrderedDict(sorted(track.items()))

        # def should_fail():
        #     """
        #     Return true randomly.
        #     """
        #     return random.randint(0, 1) == 1

        # if should_fail():
        #     raise Exception("Failed to insert track")

        # def force_surrogatepass(string: str):
        #     return string.encode("utf-16", "surrogatepass").decode("utf-16")

        track["artist"] = track["artists"]
        track["albumartist"] = track["albumartists"]

        del track["artists"]
        del track["albumartists"]

        cur.execute(sql, track)

    @classmethod
    def insert_many_tracks(cls, tracks: list[dict]):
        """
        Inserts a list of tracks into the database.
        """


        with SQLiteManager() as cur:
            for track in tracks:
                try:
                    cls.insert_one_track(track, cur)
                except Exception:
                    pprint(track, indent=4)

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
            cur.execute("SELECT * FROM tracks WHERE trackhash=?", (trackhash,))
            row = cur.fetchone()

            if row is not None:
                return tuple_to_track(row)

            return None

    @staticmethod
    def remove_tracks_by_filepaths(filepaths: str | set[str]):
        """
        Removes a track or tracks from the database using their filepaths.
        """
        if isinstance(filepaths, str):
            filepaths = {filepaths}

        with SQLiteManager() as cur:
            for filepath in filepaths:
                cur.execute("DELETE FROM tracks WHERE filepath=?", (filepath,))

    @staticmethod
    def remove_tracks_by_folders(folders: set[str]):
        sql = "DELETE FROM tracks WHERE folder = ?"

        with SQLiteManager() as cur:
            for folder in folders:
                cur.execute(sql, (folder,))
