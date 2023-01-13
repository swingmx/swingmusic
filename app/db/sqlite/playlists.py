import json
from collections import OrderedDict

from app.db.sqlite.tracks import SQLiteTrackMethods
from app.db.sqlite.utils import SQLiteManager
from app.db.sqlite.utils import tuple_to_playlist
from app.db.sqlite.utils import tuples_to_playlists
from app.models import Artist
from app.utils import background


class SQLitePlaylistMethods:
    """
    This class contains methods for interacting with the playlists table.
    """

    @staticmethod
    def insert_one_playlist(playlist: dict):
        sql = """INSERT INTO playlists(
            artisthashes,
            banner_pos,
            has_gif,
            image,
            last_updated,
            name,
            trackhashes
            ) VALUES(?,?,?,?,?,?,?)
            """

        playlist = OrderedDict(sorted(playlist.items()))
        params = (*playlist.values(), )

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, params)
            pid = cur.lastrowid
            params = (pid, *params)

            return tuple_to_playlist(params)

    @staticmethod
    def get_playlist_by_name(name: str):
        sql = "SELECT * FROM playlists WHERE name = ?"

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, (name, ))

            data = cur.fetchone()

            if data is not None:
                return tuple_to_playlist(data)

            return None

    @staticmethod
    def count_playlist_by_name(name: str):
        sql = "SELECT COUNT(*) FROM playlists WHERE name = ?"

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, (name, ))

            data = cur.fetchone()

            return int(data[0])

    @staticmethod
    def get_all_playlists():
        with SQLiteManager(userdata_db=True) as cur:
            cur.execute("SELECT * FROM playlists")
            playlists = cur.fetchall()

            if playlists is not None:
                return tuples_to_playlists(playlists)

            return []

    @staticmethod
    def get_playlist_by_id(playlist_id: int):
        sql = "SELECT * FROM playlists WHERE id = ?"

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, (playlist_id, ))

            data = cur.fetchone()

            if data is not None:
                return tuple_to_playlist(data)

            return None

    # FIXME: Extract the "add_track_to_playlist" method to use it for both the artisthash and trackhash lists.

    @staticmethod
    def add_item_to_json_list(playlist_id: int, field: str, items: list[str]):
        """
        Adds a string item to a json dumped list using a playlist id and field name. Takes the playlist ID, a field name, an item to add to the field, and an error to raise if the item is already in the field.

        Parameters
        ----------
        playlist_id : int
            The ID of the playlist to add the item to.
        field : str
            The field in the database that you want to add the item to.
        item : str
            The item to add to the list.
        error : Exception
            The error to raise if the item is already in the list.

        Returns
        -------
            A list of strings.

        """
        sql = f"SELECT {field} FROM playlists WHERE id = ?"

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, (playlist_id, ))
            data = cur.fetchone()

            if data is not None:
                db_items: list[str] = json.loads(data[0])

                for item in items:
                    if item in db_items:
                        items.remove(item)

                db_items.extend(items)

                sql = f"UPDATE playlists SET {field} = ? WHERE id = ?"
                cur.execute(sql, (json.dumps(db_items), playlist_id))
                return len(items)

    @classmethod
    def add_tracks_to_playlist(cls, playlist_id: int, trackhashes: list[str]):
        return cls.add_item_to_json_list(playlist_id, "trackhashes",
                                         trackhashes)

    @classmethod
    @background
    def add_artist_to_playlist(cls, playlist_id: int, trackhash: str):
        track = SQLiteTrackMethods.get_track_by_trackhash(trackhash)
        if track is None:
            return

        artists: list[Artist] = track.artist  # type: ignore
        artisthashes = [a.artisthash for a in artists]

        cls.add_item_to_json_list(playlist_id, "artisthashes", artisthashes)

    @staticmethod
    def update_playlist(playlist_id: int, playlist: dict):
        sql = """UPDATE playlists SET
            has_gif = ?,
            image = ?,
            last_updated = ?,
            name = ?
            WHERE id = ?
            """

        del playlist["id"]
        del playlist["trackhashes"]
        del playlist["artisthashes"]
        del playlist["banner_pos"]

        playlist = OrderedDict(sorted(playlist.items()))
        params = (*playlist.values(), playlist_id)

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, params)

    @staticmethod
    def delete_playlist(pid: str):
        sql = "DELETE FROM playlists WHERE id = ?"

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, (pid, ))

    @staticmethod
    def update_banner_pos(playlistid: int, pos: int):
        sql = """UPDATE playlists SET banner_pos = ? WHERE id = ?"""

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, (pos, playlistid))
