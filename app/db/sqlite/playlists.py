import json
from collections import OrderedDict

from app.db.sqlite.utils import SQLiteManager, tuple_to_playlist, tuples_to_playlists
from app.utils.dates import create_new_date


class SQLitePlaylistMethods:
    """
    This class contains methods for interacting with the playlists table.
    """

    @staticmethod
    def update_last_updated(playlist_id: int):
        """Updates the last updated date of a playlist."""
        sql = """UPDATE playlists SET last_updated = ? WHERE id = ?"""

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, (create_new_date(), playlist_id))

    @staticmethod
    def insert_one_playlist(playlist: dict):
        # banner_pos,
        # has_gif,
        sql = """INSERT INTO playlists(
        image,
        last_updated,
        name,
        settings,
        trackhashes
        ) VALUES(:image, :last_updated, :name, :settings, :trackhashes)
        """

        playlist = OrderedDict(sorted(playlist.items()))

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, playlist)
            pid = cur.lastrowid
            cur.close()

            p_tuple = (pid, *playlist.values())
            return tuple_to_playlist(p_tuple)

    @staticmethod
    def get_playlist_by_name(name: str):
        sql = "SELECT * FROM playlists WHERE name = ?"

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, (name,))

            data = cur.fetchone()
            cur.close()

            if data is not None:
                return tuple_to_playlist(data)

            return None

    @staticmethod
    def count_playlist_by_name(name: str):
        sql = "SELECT COUNT(*) FROM playlists WHERE name = ?"

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, (name,))

            data = cur.fetchone()
            cur.close()

            return int(data[0])

    @staticmethod
    def get_all_playlists():
        with SQLiteManager(userdata_db=True) as cur:
            cur.execute("SELECT * FROM playlists")
            playlists = cur.fetchall()
            cur.close()

            if playlists is not None:
                return tuples_to_playlists(playlists)

            return []

    @staticmethod
    def get_playlist_by_id(playlist_id: int):
        sql = "SELECT * FROM playlists WHERE id = ?"

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, (playlist_id,))

            data = cur.fetchone()
            cur.close()

            if data is not None:
                return tuple_to_playlist(data)

            return None

    # FIXME: Extract the "add_track_to_playlist" method to use it for both the artisthash and trackhash lists.

    @classmethod
    def add_item_to_json_list(cls, playlist_id: int, field: str, items: set[str]):
        """
        Adds a string item to a json dumped list using a playlist id and field name.
        Takes the playlist ID, a field name, an item to add to the field.
        """
        sql = f"SELECT {field} FROM playlists WHERE id = ?"

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, (playlist_id,))
            data = cur.fetchone()

            if data is not None:
                db_items: list[str] = json.loads(data[0])

                # Remove duplicates, without changing the order.
                for item in items:
                    if item in db_items:
                        items.remove(item)

                db_items.extend(items)

                sql = f"UPDATE playlists SET {field} = ? WHERE id = ?"
                cur.execute(sql, (json.dumps(db_items), playlist_id))
                return len(items)

        cls.update_last_updated(playlist_id)

    @classmethod
    def add_tracks_to_playlist(cls, playlist_id: int, trackhashes: list[str]):
        """
        Adds trackhashes to a playlist
        """
        return cls.add_item_to_json_list(playlist_id, "trackhashes", trackhashes)

    @classmethod
    def update_playlist(cls, playlist_id: int, playlist: dict):
        sql = """UPDATE playlists SET
            image = ?,
            last_updated = ?,
            name = ?,
            settings = ?
            WHERE id = ?
            """

        del playlist["id"]
        del playlist["trackhashes"]
        playlist["settings"] = json.dumps(playlist["settings"])

        playlist = OrderedDict(sorted(playlist.items()))
        params = (*playlist.values(), playlist_id)

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, params)

        cls.update_last_updated(playlist_id)

    @classmethod
    def update_settings(cls, playlist_id: int, settings: dict):
        sql = """UPDATE playlists SET settings = ? WHERE id = ?"""

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, (json.dumps(settings), playlist_id))

        cls.update_last_updated(playlist_id)

    @staticmethod
    def delete_playlist(pid: str):
        sql = "DELETE FROM playlists WHERE id = ?"

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, (pid,))

    @staticmethod
    def remove_banner(playlistid: int):
        sql = """UPDATE playlists SET image = NULL WHERE id = ?"""

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, (playlistid,))

    @classmethod
    def remove_tracks_from_playlist(cls, playlistid: int, tracks: list[dict[str, int]]):
        """
        Removes tracks from a playlist by trackhash and position.
        """

        sql = """UPDATE playlists SET trackhashes = ? WHERE id = ?"""

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute("SELECT trackhashes FROM playlists WHERE id = ?", (playlistid,))
            data = cur.fetchone()

            if data is None:
                return

            trackhashes: list[str] = json.loads(data[0])

            for track in tracks:
                # {
                #    trackhash: str;
                #    index: int;
                # }

                index = trackhashes.index(track["trackhash"])

                if index == track["index"]:
                    trackhashes.remove(track["trackhash"])

            cur.execute(sql, (json.dumps(trackhashes), playlistid))

        cls.update_last_updated(playlistid)
